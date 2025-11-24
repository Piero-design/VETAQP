from rest_framework import serializers
from apps.chat.models import ChatRoom, ChatMessage
from django.contrib.auth.models import User


class UserMinimalSerializer(serializers.ModelSerializer):
    """Serializer minimalista para usuarios"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class ChatMessageSerializer(serializers.ModelSerializer):
    """Serializer para mensajes de chat"""
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    sender_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatMessage
        fields = [
            'id', 'sender', 'sender_username', 'sender_name',
            'message', 'is_read', 'timestamp'
        ]
        read_only_fields = ['id', 'sender', 'timestamp']
    
    def get_sender_name(self, obj):
        """Obtiene el nombre completo del remitente"""
        if obj.sender.first_name or obj.sender.last_name:
            return f"{obj.sender.first_name} {obj.sender.last_name}".strip()
        return obj.sender.username


class ChatRoomSerializer(serializers.ModelSerializer):
    """Serializer para salas de chat"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    veterinarian_username = serializers.CharField(source='veterinarian.username', read_only=True)
    veterinarian_name = serializers.SerializerMethodField()
    last_message_text = serializers.SerializerMethodField()
    last_message_time = serializers.SerializerMethodField()
    unread_count = serializers.IntegerField(read_only=True)
    room_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = ChatRoom
        fields = [
            'id', 'user', 'user_username', 'veterinarian', 'veterinarian_username',
            'veterinarian_name', 'is_active', 'room_name', 'last_message_text',
            'last_message_time', 'unread_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_veterinarian_name(self, obj):
        """Obtiene el nombre del veterinario"""
        if obj.veterinarian.first_name or obj.veterinarian.last_name:
            return f"{obj.veterinarian.first_name} {obj.veterinarian.last_name}".strip()
        return obj.veterinarian.username
    
    def get_last_message_text(self, obj):
        """Obtiene el texto del último mensaje"""
        last_msg = obj.last_message
        if last_msg:
            return last_msg.message[:50] + ('...' if len(last_msg.message) > 50 else '')
        return None
    
    def get_last_message_time(self, obj):
        """Obtiene la fecha del último mensaje"""
        last_msg = obj.last_message
        return last_msg.timestamp.isoformat() if last_msg else None


class ChatRoomCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear salas de chat"""
    
    class Meta:
        model = ChatRoom
        fields = ['veterinarian']
    
    def validate_veterinarian(self, value):
        """Valida que el veterinario sea staff"""
        if not value.is_staff:
            raise serializers.ValidationError(
                "El usuario seleccionado no es un veterinario."
            )
        return value
    
    def validate(self, attrs):
        """Valida que no exista ya una sala activa entre el usuario y el veterinario"""
        request = self.context.get('request')
        veterinarian = attrs.get('veterinarian')
        
        if request and veterinarian:
            existing_room = ChatRoom.objects.filter(
                user=request.user,
                veterinarian=veterinarian,
                is_active=True
            ).first()
            
            if existing_room:
                raise serializers.ValidationError(
                    f"Ya tienes una sala de chat activa con este veterinario (ID: {existing_room.id})"
                )
        
        return attrs
    
    def create(self, validated_data):
        """Crea la sala de chat"""
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class ChatRoomDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para sala de chat con mensajes"""
    messages = ChatMessageSerializer(many=True, read_only=True)
    user_info = UserMinimalSerializer(source='user', read_only=True)
    veterinarian_info = UserMinimalSerializer(source='veterinarian', read_only=True)
    room_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = ChatRoom
        fields = [
            'id', 'user_info', 'veterinarian_info', 'is_active',
            'room_name', 'messages', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
