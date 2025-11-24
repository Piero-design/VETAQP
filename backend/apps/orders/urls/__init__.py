from django.urls import path
from apps.orders.views import (
    OrderListCreateView, 
    OrderDetailView, 
    OrderTrackingView,
    ShippingUpdateView,
    MyOrdersView
)

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/shipping/', ShippingUpdateView.as_view(), name='order-shipping-update'),
    path('orders/my-orders/', MyOrdersView.as_view(), name='my-orders'),
    path('orders/tracking/<str:tracking_number>/', OrderTrackingView.as_view(), name='order-tracking'),
]
