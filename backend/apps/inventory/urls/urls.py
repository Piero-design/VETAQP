from django.urls import path
from apps.inventory.views import StockMovementListCreateView, StockMovementDetailView

urlpatterns = [
    path('movements/', StockMovementListCreateView.as_view(), name='stock_movement_list_create'),
    path('movements/<int:pk>/', StockMovementDetailView.as_view(), name='stock_movement_detail'),
]
