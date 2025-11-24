from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.contrib.auth.models import User

from apps.chat.models import ChatRoom, ChatMessage
from apps.chat.serializers import (
    ChatRoomSerializer,
    ChatRoomCreateSerializer,
    ChatRoomDetailSerializer,
    ChatMessageSerializer,
    UserMinimalSerializer
)


class VeterinarianListView(generics.ListAPIView):
    """
    Lista todos los veterinarios disponibles (usuarios staff)
    GET: /api/chat/veterinarians/
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserMinimalSerializer
    
    def get_queryset(self):
        return User.objects.filter(is_staff=True, is_active=True)


class ChatRoomListCreateView(generics.ListCreateAPIView):
    """
    Lista salas de chat del usuario o crea una nueva
    GET: /api/chat/rooms/
    POST: /api/chat/rooms/
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_active']
    ordering_fields = ['updated_at', 'created_at']
    ordering = ['-updated_at']
    
    def get_queryset(self):
        """Retorna salas donde el usuario es participante"""
        user = self.request.user
        if user.is_staff:
            # Veterinarios ven salas donde son el vet
            return ChatRoom.objects.filter(veterinarian=user)
        else:
            # Usuarios normales ven sus propias salas
            return ChatRoom.objects.filter(user=user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ChatRoomCreateSerializer
        return ChatRoomSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ChatRoomDetailView(generics.RetrieveUpdateAPIView):
    """
    Obtiene detalles de una sala de chat específica con mensajes
    GET: /api/chat/rooms/{id}/
    PATCH: /api/chat/rooms/{id}/ (solo para cerrar la sala)
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatRoomDetailSerializer
    
    def get_queryset(self):
        """Solo permite acceder a salas donde el usuario es participante"""
        user = self.request.user
        if user.is_staff:
            return ChatRoom.objects.filter(veterinarian=user).prefetch_related('messages__sender')
        else:
            return ChatRoom.objects.filter(user=user).prefetch_related('messages__sender')
    
    def update(self, request, *args, **kwargs):
        """Solo permite cambiar is_active"""
        instance = self.get_object()
        
        if 'is_active' in request.data:
            instance.is_active = request.data['is_active']
            instance.save(update_fields=['is_active'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ChatMessageListView(generics.ListAPIView):
    """
    Lista mensajes de una sala específica
    GET: /api/chat/rooms/{room_id}/messages/
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatMessageSerializer
    ordering = ['timestamp']
    
    def get_queryset(self):
        room_id = self.kwargs.get('room_id')
        user = self.request.user
        
        # Verificar que el usuario tenga acceso a la sala
        if user.is_staff:
            room_exists = ChatRoom.objects.filter(
                id=room_id,
                veterinarian=user
            ).exists()
        else:
            room_exists = ChatRoom.objects.filter(
                id=room_id,
                user=user
            ).exists()
        
        if not room_exists:
            return ChatMessage.objects.none()
        
        return ChatMessage.objects.filter(room_id=room_id).select_related('sender')


class MarkMessagesAsReadView(APIView):
    """
    Marca todos los mensajes de una sala como leídos
    POST: /api/chat/rooms/{room_id}/mark-as-read/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, room_id):
        user = request.user
        
        # Verificar acceso a la sala
        try:
            if user.is_staff:
                room = ChatRoom.objects.get(id=room_id, veterinarian=user)
            else:
                room = ChatRoom.objects.get(id=room_id, user=user)
        except ChatRoom.DoesNotExist:
            return Response(
                {'detail': 'Sala de chat no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Marcar mensajes como leídos (excepto los propios)
        updated = ChatMessage.objects.filter(
            room=room,
            is_read=False
        ).exclude(sender=user).update(is_read=True)
        
        return Response({
            'message': f'{updated} mensajes marcados como leídos',
            'updated_count': updated
        })


class UnreadMessagesCountView(APIView):
    """
    Obtiene el conteo total de mensajes no leídos del usuario
    GET: /api/chat/unread-count/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        if user.is_staff:
            # Veterinarios: mensajes de usuarios en sus salas
            rooms = ChatRoom.objects.filter(veterinarian=user, is_active=True)
        else:
            # Usuarios: mensajes de veterinarios en sus salas
            rooms = ChatRoom.objects.filter(user=user, is_active=True)
        
        total_unread = 0
        for room in rooms:
            if user.is_staff:
                # Contar mensajes no leídos de usuarios
                count = ChatMessage.objects.filter(
                    room=room,
                    is_read=False,
                    sender=room.user
                ).count()
            else:
                # Contar mensajes no leídos de veterinarios
                count = ChatMessage.objects.filter(
                    room=room,
                    is_read=False,
                    sender=room.veterinarian
                ).count()
            total_unread += count
        
        return Response({'unread_count': total_unread})
