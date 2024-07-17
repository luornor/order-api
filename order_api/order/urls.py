from django.urls import path
from .views import RootAPIView,OrderCreateView, OrderDetailView, UserOrdersListView, OrderListView

app_name = 'order'

urlpatterns = [
    path('', RootAPIView.as_view(), name='root-api'),
    path('order-list', OrderListView.as_view(), name='order-list'),
    path('orders', OrderCreateView.as_view(), name='create-order'),
    path('orders/<int:id>', OrderDetailView.as_view(), name='order-detail'),
    path('users/<int:userId>/orders', UserOrdersListView.as_view(), name='user-orders'),
]
