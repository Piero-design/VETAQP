from rest_framework import serializers
from apps.appointments.models import Appointment
from apps.pets.models import Pet
from django.utils import timezone
from datetime import datetime, timedelta


class AppointmentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    pet_species = serializers.CharField(source='pet.species', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_past = serializers.BooleanField(read_only=True)
    is_today = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'user', 'user_username', 'pet', 'pet_name', 'pet_species',
            'appointment_date', 'appointment_time', 'reason', 'status', 'status_display',
            'veterinarian', 'notes', 'is_past', 'is_today', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'id', 'pet', 'appointment_date', 'appointment_time', 
            'reason', 'veterinarian', 'notes', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']
    
    def validate_pet(self, value):
        """Valida que la mascota pertenezca al usuario"""
        request = self.context.get('request')
        if request and not Pet.objects.filter(id=value.id, owner=request.user).exists():
            raise serializers.ValidationError("No tienes permiso para agendar citas para esta mascota.")
        return value
    
    def validate_appointment_date(self, value):
        """Valida que la fecha no sea en el pasado"""
        if value < timezone.now().date():
            raise serializers.ValidationError("No se pueden agendar citas en fechas pasadas.")
        
        # No permitir citas con más de 3 meses de anticipación
        max_date = timezone.now().date() + timedelta(days=90)
        if value > max_date:
            raise serializers.ValidationError("No se pueden agendar citas con más de 3 meses de anticipación.")
        
        return value
    
    def validate_appointment_time(self, value):
        """Valida horario de atención (8:00 AM - 8:00 PM)"""
        if value.hour < 8 or value.hour >= 20:
            raise serializers.ValidationError("El horario de atención es de 8:00 AM a 8:00 PM.")
        return value
    
    def validate(self, attrs):
        """Validación cruzada de fecha y hora"""
        appointment_date = attrs.get('appointment_date')
        appointment_time = attrs.get('appointment_time')
        
        if appointment_date and appointment_time:
            # Si la cita es hoy, verificar que la hora no haya pasado
            if appointment_date == timezone.now().date():
                appointment_datetime = datetime.combine(appointment_date, appointment_time)
                appointment_datetime = timezone.make_aware(appointment_datetime)
                
                if appointment_datetime < timezone.now():
                    raise serializers.ValidationError({
                        'appointment_time': 'No se puede agendar una cita en una hora que ya pasó.'
                    })
        
        return attrs
