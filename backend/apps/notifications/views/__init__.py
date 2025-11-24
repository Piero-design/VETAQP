from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer, NotificationCreateSerializer


class NotificationListCreateView(generics.ListCreateAPIView):
    """
    Vista para listar y crear notificaciones
    GET: Lista notificaciones del usuario autenticado
    POST: Crea una nueva notificación (solo admin)
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_read', 'notification_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Solo muestra las notificaciones del usuario autenticado"""
        return Notification.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NotificationCreateSerializer
        return NotificationSerializer


class NotificationDetailView(generics.RetrieveDestroyAPIView):
    """
    Vista para ver y eliminar una notificación específica
    GET: Obtiene detalles de una notificación
    DELETE: Elimina una notificación
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        """Solo permite acceder a las notificaciones del usuario autenticado"""
        return Notification.objects.filter(user=self.request.user)


class MarkAsReadView(APIView):
    """
    Vista para marcar una notificación como leída
    POST: /api/notifications/{id}/mark-as-read/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, user=request.user)
            notification.mark_as_read()
            serializer = NotificationSerializer(notification)
            return Response(serializer.data)
        except Notification.DoesNotExist:
            return Response(
                {'detail': 'Notificación no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )


class MarkAllAsReadView(APIView):
    """
    Vista para marcar todas las notificaciones como leídas
    POST: /api/notifications/mark-all-as-read/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        updated_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)
        
        return Response({
            'message': f'{updated_count} notificaciones marcadas como leídas',
            'updated_count': updated_count
        })


class UnreadCountView(APIView):
    """
    Vista para obtener el conteo de notificaciones no leídas
    GET: /api/notifications/unread-count/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        
        return Response({'unread_count': count})
