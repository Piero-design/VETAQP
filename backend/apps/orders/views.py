from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer, OrderItemSerializer
from apps.products.models import Product
import uuid

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        subtotal = 0
        order_items_data = []
        
        for item in data['items']:
            try:
                product = Product.objects.get(id=item['product_id'])
                quantity = item['quantity']
                
                if quantity <= 0:
                    return Response(
                        {'error': f'Cantidad inválida para {product.name}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                if product.stock < quantity:
                    return Response(
                        {'error': f'Stock insuficiente para {product.name}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                price = product.get_final_price()
                item_subtotal = float(price) * quantity
                subtotal += item_subtotal
                
                order_items_data.append({
                    'product': product,
                    'quantity': quantity,
                    'price': price
                })
            except Product.DoesNotExist:
                return Response(
                    {'error': f'Producto {item["product_id"]} no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        shipping_cost = 0
        tax = float(subtotal) * 0.18
        total = float(subtotal) + shipping_cost + tax
        
        order = Order.objects.create(
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            user=request.user,
            shipping_name=data['shipping_name'],
            shipping_email=data['shipping_email'],
            shipping_phone=data['shipping_phone'],
            shipping_address=data['shipping_address'],
            shipping_city=data['shipping_city'],
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax=tax,
            total=total,
            status='pending',
            payment_status='pending'
        )
        
        for item_data in order_items_data:
            OrderItem.objects.create(
                order=order,
                product=item_data['product'],
                quantity=item_data['quantity'],
                price=item_data['price']
            )
            item_data['product'].stock -= item_data['quantity']
            item_data['product'].save()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk=None):
        order = self.get_object()
        order.payment_status = 'completed'
        order.status = 'confirmed'
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)
