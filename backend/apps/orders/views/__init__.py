from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer, OrderCreateSerializer, ShippingUpdateSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'shipping_status']
    
    def get_queryset(self):
        """Los usuarios ven solo sus pedidos, los admin ven todos"""
        if self.request.user.is_staff:
            return Order.objects.all().prefetch_related('items__product')
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        """Los usuarios ven solo sus pedidos, los admin ven todos"""
        if self.request.user.is_staff:
            return Order.objects.all().prefetch_related('items__product')
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')
    
    def update(self, request, *args, **kwargs):
        """Solo permite actualizar el status"""
        instance = self.get_object()
        
        # Solo admin puede cambiar status
        if not request.user.is_staff:
            return Response(
                {"detail": "No tienes permiso para actualizar el pedido."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Solo permitir cambio de status
        if 'status' in request.data:
            instance.status = request.data['status']
            instance.save()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class OrderTrackingView(generics.RetrieveAPIView):
    """
    Vista para tracking de pedidos por número de seguimiento.
    Permite a usuarios consultar el estado de su pedido sin autenticación si tienen el tracking number.
    """
    serializer_class = OrderSerializer
    lookup_field = 'tracking_number'
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Order.objects.prefetch_related('items__product').all()


class ShippingUpdateView(generics.UpdateAPIView):
    """
    Vista para actualizar información de envío (solo staff).
    Permite actualizar shipping_status, tracking_number, fechas, etc.
    """
    serializer_class = ShippingUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = Order.objects.all()
    
    def perform_update(self, serializer):
        # Si se marca como SHIPPED y no tiene shipped_date, asignar fecha actual
        if serializer.validated_data.get('shipping_status') == 'SHIPPED':
            if not serializer.validated_data.get('shipped_date') and not serializer.instance.shipped_date:
                from django.utils import timezone
                serializer.validated_data['shipped_date'] = timezone.now()
        
        serializer.save()


class MyOrdersView(generics.ListAPIView):
    """
    Vista para que el usuario vea sus propios pedidos con información de envío.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'shipping_status']
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product').order_by('-created_at')
