from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from apps.appointments.models import Appointment
from apps.appointments.serializers import AppointmentSerializer, AppointmentCreateSerializer


class AppointmentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'appointment_date', 'pet']
    ordering_fields = ['appointment_date', 'appointment_time', 'created_at']
    ordering = ['appointment_date', 'appointment_time']
    
    def get_queryset(self):
        """Los usuarios ven solo sus citas, los admin ven todas"""
        if self.request.user.is_staff:
            return Appointment.objects.all().select_related('user', 'pet')
        return Appointment.objects.filter(user=self.request.user).select_related('user', 'pet')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AppointmentCreateSerializer
        return AppointmentSerializer
    
    def get_serializer_context(self):
        """Pasar el request al serializer para validaciones"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppointmentSerializer
    
    def get_queryset(self):
        """Los usuarios ven solo sus citas, los admin ven todas"""
        if self.request.user.is_staff:
            return Appointment.objects.all().select_related('user', 'pet')
        return Appointment.objects.filter(user=self.request.user).select_related('user', 'pet')
    
    def update(self, request, *args, **kwargs):
        """Permitir actualización parcial"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Los usuarios no pueden cambiar citas completadas o canceladas
        if not request.user.is_staff and instance.status in ['COMPLETED', 'CANCELLED']:
            return Response(
                {"detail": "No se puede modificar una cita completada o cancelada."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """Cancelar en lugar de eliminar"""
        instance = self.get_object()
        
        # Solo permitir cancelar si no está completada o ya cancelada
        if instance.status in ['COMPLETED', 'CANCELLED']:
            return Response(
                {"detail": "No se puede cancelar una cita completada o ya cancelada."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        instance.status = 'CANCELLED'
        instance.save()
        
        return Response(
            {"detail": "Cita cancelada exitosamente."},
            status=status.HTTP_200_OK
        )
