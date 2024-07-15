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
            "orders": reverse_lazy('order:order-list'),
            "create_order": reverse_lazy('order:order-create'),
            "order_detail": reverse_lazy('order:order-detail', kwargs={'id': 1}),
            "user_orders": reverse_lazy('order:user-orders', kwargs={'userId': 1})
        }
        return Response(api_urls, status=status.HTTP_200_OK)


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a new order",
        request_body=OrderSerializer,
        responses={
            201: openapi.Response('Order created successfully', OrderSerializer),
            400: 'Bad Request'
        }
    )

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

    @swagger_auto_schema(
        operation_summary="Retrieve an order by ID",
        responses={
            200: openapi.Response('Order retrieved successfully', OrderSerializer),
            404: 'Not Found'
        }
    )

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

    @swagger_auto_schema(
        operation_summary="Update an order by ID",
        request_body=OrderSerializer,
        responses={
            200: openapi.Response('Order updated successfully', OrderSerializer),
            400: 'Bad Request',
            404: 'Not Found'
        }
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

    @swagger_auto_schema(
        operation_summary="Delete an order by ID",
        responses={
            204: 'Order deleted successfully',
            404: 'Not Found'
        }
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
    
    @swagger_auto_schema(
        operation_summary="Retrieve all orders for a specific user",
        responses={
            200: openapi.Response('Orders retrieved successfully', OrderSerializer(many=True)),
            404: 'No orders found for the specified user'
        }
    )
    
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

