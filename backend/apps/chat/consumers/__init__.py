import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from apps.chat.models import ChatRoom, ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket Consumer para chat en tiempo real
    """
    
    async def connect(self):
        """Conecta al WebSocket y se une al room group"""
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = self.scope['user']
        
        # Verificar que el usuario esté autenticado
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Verificar que el usuario tenga acceso a esta sala
        has_access = await self.check_room_access()
        if not has_access:
            await self.close()
            return
        
        # Unirse al room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Marcar mensajes como leídos cuando se conecta
        await self.mark_messages_as_read()
    
    async def disconnect(self, close_code):
        """Desconecta del WebSocket"""
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """Recibe mensaje del WebSocket"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type', 'chat_message')
            
            if message_type == 'chat_message':
                message_text = data.get('message', '').strip()
                
                if not message_text:
                    await self.send(text_data=json.dumps({
                        'type': 'error',
                        'message': 'El mensaje no puede estar vacío'
                    }))
                    return
                
                # Guardar mensaje en la base de datos
                message_obj = await self.save_message(message_text)
                
                if message_obj:
                    # Enviar mensaje al room group
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': message_text,
                            'sender_id': self.user.id,
                            'sender_username': self.user.username,
                            'message_id': message_obj['id'],
                            'timestamp': message_obj['timestamp'],
                            'is_read': False
                        }
                    )
            
            elif message_type == 'mark_as_read':
                message_id = data.get('message_id')
                if message_id:
                    await self.mark_message_read(message_id)
                    
                    # Notificar al remitente que el mensaje fue leído
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'message_read',
                            'message_id': message_id
                        }
                    )
        
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Formato de mensaje inválido'
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': str(e)
            }))
    
    async def chat_message(self, event):
        """Envía mensaje al WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username'],
            'message_id': event['message_id'],
            'timestamp': event['timestamp'],
            'is_read': event['is_read']
        }))
    
    async def message_read(self, event):
        """Notifica que un mensaje fue leído"""
        await self.send(text_data=json.dumps({
            'type': 'message_read',
            'message_id': event['message_id']
        }))
    
    @database_sync_to_async
    def check_room_access(self):
        """Verifica que el usuario tenga acceso a la sala"""
        try:
            room = ChatRoom.objects.get(id=self.room_id)
            return room.user == self.user or room.veterinarian == self.user
        except ChatRoom.DoesNotExist:
            return False
    
    @database_sync_to_async
    def save_message(self, message_text):
        """Guarda el mensaje en la base de datos"""
        try:
            room = ChatRoom.objects.get(id=self.room_id)
            message = ChatMessage.objects.create(
                room=room,
                sender=self.user,
                message=message_text
            )
            # Actualizar timestamp de la sala
            room.save(update_fields=['updated_at'])
            
            return {
                'id': message.id,
                'timestamp': message.timestamp.isoformat()
            }
        except Exception as e:
            print(f"Error saving message: {e}")
            return None
    
    @database_sync_to_async
    def mark_messages_as_read(self):
        """Marca todos los mensajes recibidos como leídos"""
        try:
            room = ChatRoom.objects.get(id=self.room_id)
            # Marcar como leídos los mensajes que NO son del usuario actual
            ChatMessage.objects.filter(
                room=room,
                is_read=False
            ).exclude(sender=self.user).update(is_read=True)
        except Exception as e:
            print(f"Error marking messages as read: {e}")
    
    @database_sync_to_async
    def mark_message_read(self, message_id):
        """Marca un mensaje específico como leído"""
        try:
            message = ChatMessage.objects.get(id=message_id)
            if message.sender != self.user:
                message.mark_as_read()
        except ChatMessage.DoesNotExist:
            pass
