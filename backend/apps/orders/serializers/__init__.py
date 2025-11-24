from rest_framework import serializers
from apps.orders.models import Order, OrderItem
from apps.products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.SerializerMethodField()
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 'quantity', 'unit_price', 'subtotal']
        read_only_fields = ['id', 'subtotal']
    
    def get_product_image(self, obj):
        if obj.product.image:
            return obj.product.image.url
        return None


class OrderSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    shipping_status_display = serializers.CharField(source='get_shipping_status_display', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    is_trackable = serializers.BooleanField(read_only=True)
    can_be_delivered = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_username', 'status', 'status_display',
            'total', 'notes', 'items', 'created_at', 'updated_at',
            'shipping_status', 'shipping_status_display', 'tracking_number',
            'shipping_address', 'estimated_delivery_date', 'shipped_date',
            'delivered_date', 'is_trackable', 'can_be_delivered'
        ]
        read_only_fields = ['id', 'user', 'total', 'created_at', 'updated_at']


class ShippingUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar información de envío (solo staff)"""
    class Meta:
        model = Order
        fields = [
            'shipping_status', 'tracking_number', 'shipping_address',
            'estimated_delivery_date', 'shipped_date', 'delivered_date'
        ]
    
    def validate(self, data):
        """Validaciones para actualización de envío"""
        # Si se marca como SHIPPED, debe tener tracking_number y shipped_date
        if data.get('shipping_status') == 'SHIPPED':
            if not data.get('tracking_number') and not self.instance.tracking_number:
                raise serializers.ValidationError({
                    "tracking_number": "Se requiere número de seguimiento al marcar como enviado."
                })
        
        # Si se marca como DELIVERED, debe tener delivered_date
        if data.get('shipping_status') == 'DELIVERED':
            if not data.get('delivered_date') and not self.instance.delivered_date:
                from django.utils import timezone
                data['delivered_date'] = timezone.now()
        
        return data


class OrderItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    
    def validate_product_id(self, value):
        """Valida que el producto exista"""
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Producto con ID {value} no existe.")
        return value
    
    def validate_quantity(self, value):
        """Valida que la cantidad sea positiva"""
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a cero.")
        return value


class OrderCreateSerializer(serializers.ModelSerializer):
    items_data = OrderItemCreateSerializer(many=True, write_only=True, source='items')
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'notes', 'items_data', 'items', 'total', 'status', 'created_at']
        read_only_fields = ['id', 'total', 'status', 'created_at', 'items']
    
    def validate_items(self, value):
        """Valida que haya al menos un item"""
        if not value or len(value) == 0:
            raise serializers.ValidationError("El pedido debe tener al menos un producto.")
        return value
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Crear el pedido
        order = Order.objects.create(**validated_data)
        
        # Crear los items del pedido
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            
            # Validar stock disponible
            if product.stock < item_data['quantity']:
                order.delete()  # Eliminar pedido si no hay stock
                raise serializers.ValidationError(
                    f"Stock insuficiente para {product.name}. "
                    f"Disponible: {product.stock}, Solicitado: {item_data['quantity']}"
                )
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                unit_price=product.price
            )
            
            # Reducir stock del producto
            product.stock -= item_data['quantity']
            product.save()
        
        # Calcular y guardar el total
        order.calculate_total()
        
        return order
