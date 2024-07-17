from django.urls import path
from .views import RootAPIView,OrderCreateView, OrderDetailView, UserOrdersListView

urlpatterns = [
    path('', RootAPIView.as_view(), name='root-api'),
    path('orders', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:id>', OrderDetailView.as_view(), name='order-detail'),
    path('users/<int:userId>/orders', UserOrdersListView.as_view(), name='user-orders'),
]
