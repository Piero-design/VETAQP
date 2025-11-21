from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from apps.payments.models import Payment
from apps.payments.serializers import PaymentSerializer, PaymentCreateSerializer


class PaymentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_method']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Los usuarios ven solo sus pagos, admins ven todos
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PaymentCreateSerializer
        return PaymentSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=self.request.user)
