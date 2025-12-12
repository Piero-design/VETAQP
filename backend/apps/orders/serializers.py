from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price', 'subtotal']
    
    def get_subtotal(self, obj):
        return str(obj.get_subtotal())

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'shipping_name', 'shipping_email',
            'shipping_phone', 'shipping_address', 'shipping_city', 'subtotal',
            'shipping_cost', 'tax', 'total', 'status', 'payment_status',
            'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'order_number', 'user', 'created_at', 'updated_at']

class OrderCreateSerializer(serializers.Serializer):
    shipping_name = serializers.CharField(max_length=200)
    shipping_email = serializers.EmailField()
    shipping_phone = serializers.CharField(max_length=20)
    shipping_address = serializers.TextField()
    shipping_city = serializers.CharField(max_length=100)
    items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField(),
            required=['product_id', 'quantity']
        )
    )
    
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("El carrito no puede estar vacío")
        return value
