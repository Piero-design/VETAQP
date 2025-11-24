from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ChatRoom(models.Model):
    """
    Sala de chat entre un usuario y un veterinario
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_rooms_as_user',
        verbose_name='Usuario'
    )
    veterinarian = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_rooms_as_vet',
        verbose_name='Veterinario',
        limit_choices_to={'is_staff': True}
    )
    is_active = models.BooleanField(default=True, verbose_name='Activa')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Sala de Chat'
        verbose_name_plural = 'Salas de Chat'
        unique_together = ['user', 'veterinarian']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['veterinarian', 'is_active']),
            models.Index(fields=['-updated_at']),
        ]
    
    def __str__(self):
        return f"Chat: {self.user.username} <-> {self.veterinarian.username}"
    
    @property
    def room_name(self):
        """Genera un nombre único para el room WebSocket"""
        return f"chat_{self.id}"
    
    @property
    def last_message(self):
        """Obtiene el último mensaje de la sala"""
        return self.messages.order_by('-timestamp').first()
    
    @property
    def unread_count(self):
        """Cuenta mensajes no leídos para el usuario"""
        return self.messages.filter(sender=self.veterinarian, is_read=False).count()


class ChatMessage(models.Model):
    """
    Mensaje individual en una sala de chat
    """
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Sala'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='Remitente'
    )
    message = models.TextField(verbose_name='Mensaje')
    is_read = models.BooleanField(default=False, verbose_name='Leído')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora')
    
    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Mensaje de Chat'
        verbose_name_plural = 'Mensajes de Chat'
        indexes = [
            models.Index(fields=['room', 'timestamp']),
            models.Index(fields=['sender', 'timestamp']),
            models.Index(fields=['room', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.sender.username}: {self.message[:50]}"
    
    def mark_as_read(self):
        """Marca el mensaje como leído"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])
