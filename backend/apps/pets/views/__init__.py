from rest_framework import generics, filters, permissions
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from apps.pets.models import Pet, MedicalRecord, Vaccine
from apps.pets.serializers import PetSerializer
from apps.pets.serializers import (
    PetDetailSerializer, MedicalRecordSerializer, VaccineSerializer
)


# Original Pet views
class PetListCreateView(generics.ListCreateAPIView):
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Cada usuario solo ve sus propias mascotas
        return Pet.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        # Al crear, asignar automáticamente al usuario actual
        serializer.save(owner=self.request.user)


class PetDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Cada usuario solo puede acceder a sus propias mascotas
        return Pet.objects.filter(owner=self.request.user)


# Medical Records views
class MedicalRecordListCreateView(generics.ListCreateAPIView):
    """
    Lista y crea registros médicos.
    - Staff: puede ver y crear registros de todas las mascotas
    - Usuario: solo puede ver registros de sus propias mascotas
    """
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['pet', 'date']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date', '-created_at']
    
    def get_queryset(self):
        user = self.request.user
        # Staff puede ver todos los registros
        if user.is_staff:
            return MedicalRecord.objects.select_related('pet', 'pet__owner').all()
        # Usuario normal solo ve registros de sus mascotas
        return MedicalRecord.objects.select_related('pet', 'pet__owner').filter(pet__owner=user)


class MedicalRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalle, actualiza y elimina un registro médico.
    - Staff: puede ver, editar y eliminar todos los registros
    - Usuario: solo puede ver registros de sus propias mascotas (sin editar/eliminar)
    """
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MedicalRecord.objects.select_related('pet', 'pet__owner').all()
        return MedicalRecord.objects.select_related('pet', 'pet__owner').filter(pet__owner=user)
    
    def perform_update(self, serializer):
        # Solo staff puede actualizar
        if not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Solo el personal médico puede actualizar registros.")
        serializer.save()
    
    def perform_destroy(self, instance):
        # Solo staff puede eliminar
        if not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Solo el personal médico puede eliminar registros.")
        instance.delete()


class VaccineListCreateView(generics.ListCreateAPIView):
    """
    Lista y crea registros de vacunas.
    - Staff: puede ver y crear vacunas de todas las mascotas
    - Usuario: solo puede ver vacunas de sus propias mascotas
    """
    serializer_class = VaccineSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['pet', 'vaccine_name', 'date_administered']
    ordering_fields = ['date_administered', 'next_dose_date', 'created_at']
    ordering = ['-date_administered']
    
    def get_queryset(self):
        user = self.request.user
        # Staff puede ver todas las vacunas
        if user.is_staff:
            return Vaccine.objects.select_related('pet', 'pet__owner').all()
        # Usuario normal solo ve vacunas de sus mascotas
        return Vaccine.objects.select_related('pet', 'pet__owner').filter(pet__owner=user)


class VaccineDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalle, actualiza y elimina una vacuna.
    - Staff: puede ver, editar y eliminar todas las vacunas
    - Usuario: solo puede ver vacunas de sus propias mascotas (sin editar/eliminar)
    """
    serializer_class = VaccineSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Vaccine.objects.select_related('pet', 'pet__owner').all()
        return Vaccine.objects.select_related('pet', 'pet__owner').filter(pet__owner=user)
    
    def perform_update(self, serializer):
        # Solo staff puede actualizar
        if not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Solo el personal médico puede actualizar vacunas.")
        serializer.save()
    
    def perform_destroy(self, instance):
        # Solo staff puede eliminar
        if not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Solo el personal médico puede eliminar vacunas.")
        instance.delete()


class PetMedicalHistoryView(generics.RetrieveAPIView):
    """
    Devuelve el historial médico completo de una mascota (registros + vacunas).
    - Staff: puede ver cualquier mascota
    - Usuario: solo puede ver sus propias mascotas
    """
    serializer_class = PetDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Pet.objects.prefetch_related('medical_records', 'vaccines').select_related('owner').all()
        return Pet.objects.prefetch_related('medical_records', 'vaccines').select_related('owner').filter(owner=user)
