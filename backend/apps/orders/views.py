from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer, OrderCreateSerializer


class OrderListCreateView(generics.ListCreateAPIView):
	permission_classes = [IsAuthenticated]
	filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
	filterset_fields = ['status']
	ordering_fields = ['created_at', 'total']
	ordering = ['-created_at']

	def get_queryset(self):
		user = self.request.user
		if user.is_staff:
			return Order.objects.select_related('customer')
		return Order.objects.select_related('customer').filter(customer=user)

	def get_serializer_class(self):
		if self.request.method == 'POST':
			return OrderCreateSerializer
		return OrderSerializer

	def perform_create(self, serializer):
		serializer.save(customer=self.request.user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = OrderSerializer

	def get_queryset(self):
		user = self.request.user
		if user.is_staff:
			return Order.objects.select_related('customer')
		return Order.objects.select_related('customer').filter(customer=user)
