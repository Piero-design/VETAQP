from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.appointments.models import Appointment
from apps.appointments.serializers import (
	AppointmentSerializer,
	AppointmentCreateSerializer,
)


class AppointmentListCreateView(generics.ListCreateAPIView):
	permission_classes = [IsAuthenticated]
	filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
	filterset_fields = ['status', 'pet']
	ordering_fields = ['scheduled_at', 'created_at']
	ordering = ['-scheduled_at']

	def get_queryset(self):
		user = self.request.user
		if user.is_staff:
			return Appointment.objects.select_related('owner', 'pet')
		return Appointment.objects.select_related('owner', 'pet').filter(owner=user)

	def get_serializer_class(self):
		if self.request.method == 'POST':
			return AppointmentCreateSerializer
		return AppointmentSerializer

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = AppointmentSerializer

	def get_queryset(self):
		user = self.request.user
		if user.is_staff:
			return Appointment.objects.select_related('owner', 'pet')
		return Appointment.objects.select_related('owner', 'pet').filter(owner=user)
