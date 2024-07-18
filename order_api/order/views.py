from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.urls import reverse_lazy
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Order
from .serializers import OrderSerializer
import json
from .tasks import send_to_delivery_service,update_inventory

class RootAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Root API Endpoint",
        operation_description="Provides the URLs for the available endpoints in the API.",
        responses={
            200: openapi.Response(
                'Successful operation',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "orders": openapi.Schema(type=openapi.TYPE_STRING),
                        "create_order": openapi.Schema(type=openapi.TYPE_STRING),
                        "order_detail": openapi.Schema(type=openapi.TYPE_STRING),
                        "user_orders": openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            )
        },
        tags=['Root']
    )
    def get(self, request, *args, **kwargs):
        api_urls = {
            "orders": reverse_lazy('order-list'),
            "create-order": reverse_lazy('create-order'),
            "order-detail": reverse_lazy('order-detail', kwargs={'id': 1}),
            "user-orders": reverse_lazy('user-orders', kwargs={'userId': 1})
        }
        return Response(api_urls, status=status.HTTP_200_OK)


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve all orders",
        operation_description="Retrieve all orders in the database.",
        responses={
            200: openapi.Response(
                'Orders retrieved successfully',
                OrderSerializer(many=True)
            )
        },
        tags=['Order']
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "message": "Orders retrieved successfully",
                "orders": serializer.data
            },
            status=status.HTTP_200_OK
        )  


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a new order",
        operation_description="Endpoint to create a new order. Returns a success message and the created order data.",
        request_body=OrderSerializer,
        responses={
            201: openapi.Response('Order created successfully', OrderSerializer),
            400: 'Bad Request'
        },
        tags=['Order']
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        order_data = serializer.data
        message = {
            "order_data": order_data,
        }
        
        # Send the order data to the delivery service and update the inventory
        send_to_delivery_service.delay(message)
        update_inventory.delay(message)

        return Response(
            {
                "message": "Order created successfully",
                "order": order_data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )



class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_summary="Retrieve an order by ID",
        operation_description="Retrieve detailed information of a specific order by its ID.",
        responses={
            200: openapi.Response('Order retrieved successfully', OrderSerializer),
            404: 'Not Found'
        },
        tags=['Order']
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
        operation_description="Update the details of an existing order by its ID.",
        request_body=OrderSerializer,
        responses={
            200: openapi.Response('Order updated successfully', OrderSerializer),
            400: 'Bad Request',
            404: 'Not Found'
        },
        tags=['Order']
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
        operation_summary="Partial update an order by ID",
        operation_description="Partially update the details of an existing order by its ID.",
        request_body=OrderSerializer,
        responses={
            200: openapi.Response('Order partially updated successfully', OrderSerializer),
            400: 'Bad Request',
            404: 'Not Found'
        },
        tags=['Order']
    )
    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "message": "Order partially updated successfully",
                "order": serializer.data
            },
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_summary="Delete an order by ID",
        operation_description="Delete an existing order by its ID.",
        responses={
            204: 'Order deleted successfully',
            404: 'Not Found'
        },
        tags=['Order']
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
        operation_description="Retrieve all orders associated with a specific user by their user ID.",
        responses={
            200: openapi.Response('Orders retrieved successfully', OrderSerializer(many=True)),
            404: 'No orders found for the specified user'
        },
        tags=['Order']
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
