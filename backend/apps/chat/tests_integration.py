from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from apps.chat.models import ChatRoom, ChatMessage


class ChatIntegrationTests(APITestCase):
    """
    Tests de integración para el módulo de chat
    """
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear usuarios de prueba
        self.user1 = User.objects.create_user(
            username='client1',
            email='client1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='client2',
            email='client2@example.com',
            password='testpass123'
        )
        self.vet1 = User.objects.create_user(
            username='vet1',
            email='vet1@example.com',
            password='testpass123',
            is_staff=True,
            first_name='Dr. Carlos',
            last_name='García'
        )
        self.vet2 = User.objects.create_user(
            username='vet2',
            email='vet2@example.com',
            password='testpass123',
            is_staff=True
        )
        
        # Crear sala de chat de prueba
        self.room1 = ChatRoom.objects.create(
            user=self.user1,
            veterinarian=self.vet1
        )
        
        # Crear mensajes de prueba
        self.message1 = ChatMessage.objects.create(
            room=self.room1,
            sender=self.user1,
            message='Hola, necesito una consulta'
        )
        self.message2 = ChatMessage.objects.create(
            room=self.room1,
            sender=self.vet1,
            message='Hola, dime en qué puedo ayudarte'
        )
    
    def test_list_veterinarians_requires_auth(self):
        """Test que listar veterinarios requiere autenticación"""
        response = self.client.get('/api/chat/veterinarians/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_veterinarians(self):
        """Test que lista solo veterinarios (usuarios staff)"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/chat/veterinarians/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # vet1 y vet2
        
        # Verificar que contiene campos correctos
        vet = response.data[0]
        self.assertIn('id', vet)
        self.assertIn('username', vet)
        self.assertIn('first_name', vet)
        self.assertIn('last_name', vet)
    
    def test_create_chat_room(self):
        """Test que crea una nueva sala de chat"""
        self.client.force_authenticate(user=self.user2)
        data = {'veterinarian': self.vet1.id}
        
        response = self.client.post('/api/chat/rooms/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que se creó la sala
        self.assertTrue(
            ChatRoom.objects.filter(user=self.user2, veterinarian=self.vet1).exists()
        )
    
    def test_create_chat_room_with_non_staff(self):
        """Test que no permite crear sala con usuario no staff"""
        self.client.force_authenticate(user=self.user1)
        data = {'veterinarian': self.user2.id}  # user2 no es staff
        
        response = self.client.post('/api/chat/rooms/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('veterinarian', response.data)
    
    def test_create_duplicate_chat_room(self):
        """Test que no permite crear sala duplicada"""
        self.client.force_authenticate(user=self.user1)
        data = {'veterinarian': self.vet1.id}  # Ya existe room1
        
        response = self.client.post('/api/chat/rooms/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_chat_rooms_user(self):
        """Test que lista salas de chat del usuario"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/chat/rooms/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Solo room1
        
        room = response.data[0]
        self.assertEqual(room['id'], self.room1.id)
        self.assertIn('veterinarian_username', room)
        self.assertIn('veterinarian_name', room)
        self.assertIn('last_message_text', room)
        self.assertIn('unread_count', room)
    
    def test_list_chat_rooms_veterinarian(self):
        """Test que lista salas de chat del veterinario"""
        self.client.force_authenticate(user=self.vet1)
        response = self.client.get('/api/chat/rooms/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Solo room1
    
    def test_get_chat_room_detail(self):
        """Test que obtiene detalles de una sala con mensajes"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f'/api/chat/rooms/{self.room1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('messages', response.data)
        self.assertEqual(len(response.data['messages']), 2)
        
        # Verificar estructura del mensaje
        message = response.data['messages'][0]
        self.assertIn('id', message)
        self.assertIn('sender_username', message)
        self.assertIn('message', message)
        self.assertIn('timestamp', message)
        self.assertIn('is_read', message)
    
    def test_cannot_access_other_user_chat_room(self):
        """Test que un usuario no puede acceder a salas de otros usuarios"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(f'/api/chat/rooms/{self.room1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_list_chat_messages(self):
        """Test que lista mensajes de una sala"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f'/api/chat/rooms/{self.room1.id}/messages/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verificar orden cronológico
        self.assertEqual(response.data[0]['id'], self.message1.id)
        self.assertEqual(response.data[1]['id'], self.message2.id)
    
    def test_mark_messages_as_read(self):
        """Test que marca mensajes como leídos"""
        # Verificar que message2 no está leído
        self.assertFalse(self.message2.is_read)
        
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(f'/api/chat/rooms/{self.room1.id}/mark-as-read/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('updated_count', response.data)
        self.assertEqual(response.data['updated_count'], 1)
        
        # Verificar que se marcó como leído
        self.message2.refresh_from_db()
        self.assertTrue(self.message2.is_read)
    
    def test_unread_messages_count(self):
        """Test que cuenta mensajes no leídos"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/chat/unread-count/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('unread_count', response.data)
        self.assertEqual(response.data['unread_count'], 1)  # Solo message2
    
    def test_close_chat_room(self):
        """Test que cierra una sala de chat"""
        self.client.force_authenticate(user=self.user1)
        data = {'is_active': False}
        
        response = self.client.patch(f'/api/chat/rooms/{self.room1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que se cerró
        self.room1.refresh_from_db()
        self.assertFalse(self.room1.is_active)
    
    def test_filter_chat_rooms_by_active(self):
        """Test que filtra salas activas/inactivas"""
        # Crear sala inactiva
        ChatRoom.objects.create(
            user=self.user1,
            veterinarian=self.vet2,
            is_active=False
        )
        
        self.client.force_authenticate(user=self.user1)
        
        # Filtrar activas
        response = self.client.get('/api/chat/rooms/?is_active=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Solo room1
        
        # Filtrar inactivas
        response = self.client.get('/api/chat/rooms/?is_active=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Solo la nueva


class ChatModelTests(TestCase):
    """Tests para los modelos de Chat"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.vet = User.objects.create_user(username='vet', password='pass', is_staff=True)
        self.room = ChatRoom.objects.create(user=self.user, veterinarian=self.vet)
    
    def test_room_name_property(self):
        """Test que genera el nombre del room correctamente"""
        expected = f"chat_{self.room.id}"
        self.assertEqual(self.room.room_name, expected)
    
    def test_last_message_property(self):
        """Test que obtiene el último mensaje"""
        msg1 = ChatMessage.objects.create(room=self.room, sender=self.user, message='First')
        msg2 = ChatMessage.objects.create(room=self.room, sender=self.vet, message='Second')
        
        self.assertEqual(self.room.last_message, msg2)
    
    def test_unread_count_property(self):
        """Test que cuenta mensajes no leídos"""
        # Mensajes del veterinario no leídos por el usuario
        ChatMessage.objects.create(room=self.room, sender=self.vet, message='Msg 1')
        ChatMessage.objects.create(room=self.room, sender=self.vet, message='Msg 2')
        ChatMessage.objects.create(room=self.room, sender=self.user, message='My msg')
        
        self.assertEqual(self.room.unread_count, 2)
    
    def test_mark_message_as_read(self):
        """Test que marca un mensaje como leído"""
        message = ChatMessage.objects.create(room=self.room, sender=self.vet, message='Test')
        
        self.assertFalse(message.is_read)
        message.mark_as_read()
        self.assertTrue(message.is_read)
