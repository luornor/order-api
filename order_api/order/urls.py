from django.urls import path
from .views import (
    RootAPIView,OrderListView, OrderCreateView, OrderDetailView, UserOrdersListView,
    CartListView, CartCreateView, CartItemCreateView, CartDetailView
)
app_name = 'order'

urlpatterns = [
    path('', RootAPIView.as_view(), name='root-api'),
    path('order-list/', OrderListView.as_view(), name='order-list'),
    path('orders/', OrderCreateView.as_view(), name='create-order'),
    path('orders/<int:id>', OrderDetailView.as_view(), name='order-detail'),
    path('users/<int:userId>/orders', UserOrdersListView.as_view(), name='user-orders'),
    path('cart/create/', CartCreateView.as_view(), name='cart-create'),
    path('cart/items/add/', CartItemCreateView.as_view(), name='cart-item-add'),
    path('cart/<int:user_id>/', CartListView.as_view(), name='cart-detail'),
]
