from rest_framework import serializers
from apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer para notificaciones
    """
    notification_type_display = serializers.CharField(
        source='get_notification_type_display',
        read_only=True
    )
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'title',
            'message',
            'notification_type',
            'notification_type_display',
            'is_read',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'notification_type_display']


class NotificationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear notificaciones (admin/system use)
    """
    
    class Meta:
        model = Notification
        fields = [
            'user',
            'title',
            'message',
            'notification_type',
        ]
    
    def validate_title(self, value):
        """Valida que el título no esté vacío"""
        if not value.strip():
            raise serializers.ValidationError("El título no puede estar vacío")
        return value
    
    def validate_message(self, value):
        """Valida que el mensaje no esté vacío"""
        if not value.strip():
            raise serializers.ValidationError("El mensaje no puede estar vacío")
        return value
