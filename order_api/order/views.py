from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.urls import reverse_lazy
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Order
from .serializers import OrderSerializer
import requests
from django.conf import settings


# Create your views here.

class RootAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Root API Endpoint",
        responses={200: openapi.Response('Successful operation', schema=openapi.Schema(type=openapi.TYPE_OBJECT))},
    )
    def get(self, request, *args, **kwargs):
        api_urls = {
            'register': request.build_absolute_uri(reverse_lazy('register')),
            'login': request.build_absolute_uri(reverse_lazy('login')),
            'user-detail': request.build_absolute_uri(reverse_lazy('user-detail', args=[1])),
        }
        return Response(api_urls, status=status.HTTP_200_OK)


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            "message": "Order created successfully",
            "order": serializer.data
        }, 
        status=status.HTTP_201_CREATED, headers=headers)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'  # Specify the lookup field


    def get(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "message": "Order retrieved successfully",
                "order": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def put(self, request, *args, **kwargs):
        

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "message": "Order updated successfully",
                "order": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        

        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {
                "message": "Order deleted successfully",
            },
            status=status.HTTP_204_NO_CONTENT
        )


class UserOrdersListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs['userId']
        return Order.objects.filter(user_id=user_id)
    
    def get(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if queryset.exists():
            return Response(
                {
                    "message": "Orders retrieved successfully",
                    "orders": serializer.data,
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "message": "No orders found for the specified user",
                    "orders": []
                },
                status=status.HTTP_404_NOT_FOUND
            )

