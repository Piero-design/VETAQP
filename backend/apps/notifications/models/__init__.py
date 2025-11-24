from django.db import models
from django.conf import settings


class Notification(models.Model):
    """
    Modelo para gestionar notificaciones del sistema
    """
    
    TYPE_CHOICES = [
        ('INFO', 'Información'),
        ('WARNING', 'Advertencia'),
        ('SUCCESS', 'Éxito'),
        ('ERROR', 'Error'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Usuario'
    )
    title = models.CharField(max_length=200, verbose_name='Título')
    message = models.TextField(verbose_name='Mensaje')
    notification_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='INFO',
        verbose_name='Tipo'
    )
    is_read = models.BooleanField(default=False, verbose_name='Leída')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username} ({'Leída' if self.is_read else 'No leída'})"
    
    def mark_as_read(self):
        """Marca la notificación como leída"""
        self.is_read = True
        self.save(update_fields=['is_read'])
