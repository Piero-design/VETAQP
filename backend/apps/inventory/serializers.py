from rest_framework import serializers
from .models import StockMovement
from apps.products.serializers import ProductSerializer


class StockMovementSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = StockMovement
        fields = ['id', 'product', 'product_detail', 'movement_type', 'quantity', 'reason', 'user', 'user_username', 'created_at']
        read_only_fields = ['user', 'created_at']
