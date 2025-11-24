from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.pets.models import Pet
from datetime import datetime, time


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('SCHEDULED', 'Programada'),
        ('CONFIRMED', 'Confirmada'),
        ('IN_PROGRESS', 'En Progreso'),
        ('COMPLETED', 'Completada'),
        ('CANCELLED', 'Cancelada'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    veterinarian = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['appointment_date', 'appointment_time']
    
    def __str__(self):
        return f"{self.pet.name} - {self.appointment_date} {self.appointment_time}"
    
    @property
    def is_past(self):
        """Verifica si la cita ya pasó"""
        now = timezone.now()
        appointment_datetime = datetime.combine(self.appointment_date, self.appointment_time)
        appointment_datetime = timezone.make_aware(appointment_datetime)
        return appointment_datetime < now
    
    @property
    def is_today(self):
        """Verifica si la cita es hoy"""
        return self.appointment_date == timezone.now().date()
