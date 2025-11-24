from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Notification

User = get_user_model()


class NotificationIntegrationTests(APITestCase):
    """
    Tests de integración para el módulo de notificaciones
    """
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear usuarios de prueba
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        # Crear notificaciones de prueba
        self.notification1 = Notification.objects.create(
            user=self.user1,
            title='Bienvenido',
            message='Bienvenido a AqpVet',
            notification_type='SUCCESS'
        )
        self.notification2 = Notification.objects.create(
            user=self.user1,
            title='Recordatorio',
            message='Tienes una cita mañana',
            notification_type='INFO',
            is_read=True
        )
        self.notification3 = Notification.objects.create(
            user=self.user2,
            title='Alerta',
            message='Stock bajo en productos',
            notification_type='WARNING'
        )
    
    def test_list_notifications_requires_auth(self):
        """Test que listar notificaciones requiere autenticación"""
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_user_notifications(self):
        """Test que lista solo las notificaciones del usuario autenticado"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/notifications/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Solo las de user1
        
        # Verificar que contiene los campos correctos
        notification = response.data[0]
        self.assertIn('id', notification)
        self.assertIn('title', notification)
        self.assertIn('message', notification)
        self.assertIn('notification_type', notification)
        self.assertIn('notification_type_display', notification)
        self.assertIn('is_read', notification)
        self.assertIn('created_at', notification)
    
    def test_create_notification(self):
        """Test que crea una nueva notificación"""
        self.client.force_authenticate(user=self.user1)
        data = {
            'user': self.user1.id,
            'title': 'Nueva notificación',
            'message': 'Mensaje de prueba',
            'notification_type': 'INFO'
        }
        
        response = self.client.post('/api/notifications/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Notification.objects.filter(user=self.user1).count(), 3)
        
        # Verificar que se creó correctamente
        notification = Notification.objects.get(title='Nueva notificación')
        self.assertEqual(notification.message, 'Mensaje de prueba')
        self.assertEqual(notification.notification_type, 'INFO')
        self.assertFalse(notification.is_read)
    
    def test_create_notification_validation(self):
        """Test que valida los campos al crear una notificación"""
        self.client.force_authenticate(user=self.user1)
        
        # Título vacío
        data = {
            'user': self.user1.id,
            'title': '   ',
            'message': 'Mensaje válido',
            'notification_type': 'INFO'
        }
        response = self.client.post('/api/notifications/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Mensaje vacío
        data = {
            'user': self.user1.id,
            'title': 'Título válido',
            'message': '   ',
            'notification_type': 'INFO'
        }
        response = self.client.post('/api/notifications/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_mark_notification_as_read(self):
        """Test que marca una notificación como leída"""
        self.client.force_authenticate(user=self.user1)
        
        # Verificar que está no leída
        self.assertFalse(self.notification1.is_read)
        
        response = self.client.post(f'/api/notifications/{self.notification1.id}/mark-as-read/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que se marcó como leída
        self.notification1.refresh_from_db()
        self.assertTrue(self.notification1.is_read)
    
    def test_mark_all_notifications_as_read(self):
        """Test que marca todas las notificaciones del usuario como leídas"""
        self.client.force_authenticate(user=self.user1)
        
        # Crear más notificaciones no leídas
        Notification.objects.create(
            user=self.user1,
            title='Notif 3',
            message='Mensaje 3',
            notification_type='INFO'
        )
        
        response = self.client.post('/api/notifications/mark-all-as-read/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('updated_count', response.data)
        self.assertEqual(response.data['updated_count'], 2)  # 2 no leídas de user1
        
        # Verificar que todas están leídas
        unread_count = Notification.objects.filter(user=self.user1, is_read=False).count()
        self.assertEqual(unread_count, 0)
    
    def test_filter_notifications_by_read_status(self):
        """Test que filtra notificaciones por estado de lectura"""
        self.client.force_authenticate(user=self.user1)
        
        # Filtrar no leídas
        response = self.client.get('/api/notifications/?is_read=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Solo notification1
        
        # Filtrar leídas
        response = self.client.get('/api/notifications/?is_read=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Solo notification2
    
    def test_filter_notifications_by_type(self):
        """Test que filtra notificaciones por tipo"""
        self.client.force_authenticate(user=self.user1)
        
        # Filtrar por tipo SUCCESS
        response = self.client.get('/api/notifications/?notification_type=SUCCESS')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['notification_type'], 'SUCCESS')
    
    def test_unread_count(self):
        """Test que obtiene el conteo de notificaciones no leídas"""
        self.client.force_authenticate(user=self.user1)
        
        response = self.client.get('/api/notifications/unread-count/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unread_count'], 1)
    
    def test_delete_notification(self):
        """Test que elimina una notificación"""
        self.client.force_authenticate(user=self.user1)
        
        notification_id = self.notification1.id
        response = self.client.delete(f'/api/notifications/{notification_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar que se eliminó
        self.assertFalse(Notification.objects.filter(id=notification_id).exists())
    
    def test_cannot_access_other_user_notifications(self):
        """Test que un usuario no puede acceder a notificaciones de otro usuario"""
        self.client.force_authenticate(user=self.user1)
        
        # Intentar acceder a notificación de user2
        response = self.client.get(f'/api/notifications/{self.notification3.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Intentar marcar como leída notificación de user2
        response = self.client.post(f'/api/notifications/{self.notification3.id}/mark-as-read/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
