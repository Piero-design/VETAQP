from django.db import models
from django.contrib.auth.models import User


class Pet(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')

    def __str__(self):
        return self.name


class MedicalRecord(models.Model):
    """
    Registro médico/historial clínico de una mascota
    """
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='medical_records', verbose_name='Mascota')
    date = models.DateField(verbose_name='Fecha de consulta')
    diagnosis = models.TextField(verbose_name='Diagnóstico')
    treatment = models.TextField(verbose_name='Tratamiento')
    veterinarian = models.CharField(max_length=200, verbose_name='Veterinario')
    notes = models.TextField(blank=True, verbose_name='Notas adicionales')
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Peso (kg)')
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name='Temperatura (°C)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Registro Médico'
        verbose_name_plural = 'Registros Médicos'
        indexes = [
            models.Index(fields=['pet', '-date']),
            models.Index(fields=['-date']),
        ]
    
    def __str__(self):
        return f"{self.pet.name} - {self.date} - {self.diagnosis[:50]}"


class Vaccine(models.Model):
    """
    Registro de vacunación de mascotas
    """
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='vaccines', verbose_name='Mascota')
    vaccine_name = models.CharField(max_length=200, verbose_name='Nombre de la vacuna')
    date_administered = models.DateField(verbose_name='Fecha de aplicación')
    next_dose_date = models.DateField(null=True, blank=True, verbose_name='Próxima dosis')
    veterinarian = models.CharField(max_length=200, verbose_name='Veterinario')
    batch_number = models.CharField(max_length=100, blank=True, verbose_name='Número de lote')
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    
    class Meta:
        ordering = ['-date_administered']
        verbose_name = 'Vacuna'
        verbose_name_plural = 'Vacunas'
        indexes = [
            models.Index(fields=['pet', '-date_administered']),
            models.Index(fields=['next_dose_date']),
        ]
    
    def __str__(self):
        return f"{self.pet.name} - {self.vaccine_name} - {self.date_administered}"
    
    @property
    def is_next_dose_pending(self):
        """Verifica si hay una próxima dosis pendiente"""
        from django.utils import timezone
        if self.next_dose_date:
            return self.next_dose_date >= timezone.now().date()
        return False
