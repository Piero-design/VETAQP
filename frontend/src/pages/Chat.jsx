import { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const Chat = () => {
  const [rooms, setRooms] = useState([]);
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [messages, setMessages] = useState([]);
  const [messageText, setMessageText] = useState('');
  const [veterinarians, setVeterinarians] = useState([]);
  const [showNewChatModal, setShowNewChatModal] = useState(false);
  const [selectedVet, setSelectedVet] = useState('');
  const [ws, setWs] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const messagesEndRef = useRef(null);
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    fetchCurrentUser();
    fetchRooms();
    fetchVeterinarians();
  }, []);

  useEffect(() => {
    if (selectedRoom) {
      fetchMessages(selectedRoom.id);
      connectWebSocket(selectedRoom.id);
    }
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, [selectedRoom]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchCurrentUser = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/api/users/profile/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setCurrentUser(response.data);
    } catch (error) {
      console.error('Error fetching current user:', error);
    }
  };

  const fetchRooms = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/api/chat/rooms/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setRooms(response.data);
    } catch (error) {
      console.error('Error fetching rooms:', error);
    }
  };

  const fetchVeterinarians = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/api/chat/veterinarians/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setVeterinarians(response.data);
    } catch (error) {
      console.error('Error fetching veterinarians:', error);
    }
  };

  const fetchMessages = async (roomId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`http://localhost:8000/api/chat/rooms/${roomId}/messages/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMessages(response.data);
      
      // Marcar mensajes como leídos
      await axios.post(
        `http://localhost:8000/api/chat/rooms/${roomId}/mark-as-read/`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  const connectWebSocket = (roomId) => {
    if (ws) {
      ws.close();
    }

    const token = localStorage.getItem('token');
    const wsUrl = `ws://localhost:8000/ws/chat/${roomId}/?token=${token}`;
    const websocket = new WebSocket(wsUrl);

    websocket.onopen = () => {
      console.log('WebSocket conectado');
      setIsConnected(true);
    };

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'chat_message') {
        setMessages(prev => [...prev, {
          id: data.message_id,
          sender: data.sender_id,
          sender_username: data.sender_username,
          message: data.message,
          timestamp: data.timestamp,
          is_read: data.is_read
        }]);
      } else if (data.type === 'message_read') {
        setMessages(prev => prev.map(msg =>
          msg.id === data.message_id ? { ...msg, is_read: true } : msg
        ));
      } else if (data.type === 'error') {
        console.error('WebSocket error:', data.message);
        alert(data.message);
      }
    };

    websocket.onclose = () => {
      console.log('WebSocket desconectado');
      setIsConnected(false);
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
    };

    setWs(websocket);
  };

  const sendMessage = (e) => {
    e.preventDefault();
    if (!messageText.trim() || !ws || !isConnected) return;

    ws.send(JSON.stringify({
      type: 'chat_message',
      message: messageText
    }));

    setMessageText('');
  };

  const createNewChat = async (e) => {
    e.preventDefault();
    if (!selectedVet) {
      alert('Selecciona un veterinario');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        'http://localhost:8000/api/chat/rooms/',
        { veterinarian: parseInt(selectedVet) },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      setShowNewChatModal(false);
      setSelectedVet('');
      fetchRooms();
      setSelectedRoom(response.data);
    } catch (error) {
      console.error('Error creating chat:', error);
      const errorMsg = error.response?.data?.non_field_errors?.[0] || 
                       error.response?.data?.veterinarian?.[0] ||
                       'Error al crear el chat';
      alert(errorMsg);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
  };

  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date.toDateString() === today.toDateString()) {
      return 'Hoy';
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Ayer';
    } else {
      return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'short' });
    }
  };

  return (
    <div className="h-screen flex flex-col max-w-7xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Chat con Veterinario</h1>

      <div className="flex-1 flex gap-4 overflow-hidden">
        {/* Lista de Salas */}
        <div className="w-1/3 bg-white rounded-lg shadow-md flex flex-col">
          <div className="p-4 border-b flex justify-between items-center">
            <h2 className="text-xl font-bold">Conversaciones</h2>
            <button
              onClick={() => setShowNewChatModal(true)}
              className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 text-sm"
            >
              + Nueva
            </button>
          </div>
          
          <div className="flex-1 overflow-y-auto">
            {rooms.length === 0 ? (
              <p className="p-4 text-gray-500 text-center">No hay conversaciones</p>
            ) : (
              rooms.map(room => (
                <div
                  key={room.id}
                  onClick={() => setSelectedRoom(room)}
                  className={`p-4 border-b cursor-pointer hover:bg-gray-50 transition ${
                    selectedRoom?.id === room.id ? 'bg-blue-50 border-l-4 border-l-blue-500' : ''
                  }`}
                >
                  <div className="flex justify-between items-start mb-1">
                    <h3 className="font-bold">
                      👨‍⚕️ {room.veterinarian_name || room.veterinarian_username}
                    </h3>
                    {room.unread_count > 0 && (
                      <span className="bg-red-500 text-white text-xs rounded-full px-2 py-1">
                        {room.unread_count}
                      </span>
                    )}
                  </div>
                  {room.last_message_text && (
                    <p className="text-sm text-gray-600 truncate">{room.last_message_text}</p>
                  )}
                  {room.last_message_time && (
                    <p className="text-xs text-gray-400 mt-1">
                      {formatDate(room.last_message_time)}
                    </p>
                  )}
                </div>
              ))
            )}
          </div>
        </div>

        {/* Área de Chat */}
        <div className="flex-1 bg-white rounded-lg shadow-md flex flex-col">
          {selectedRoom ? (
            <>
              {/* Header */}
              <div className="p-4 border-b flex justify-between items-center">
                <div>
                  <h2 className="text-xl font-bold">
                    👨‍⚕️ {selectedRoom.veterinarian_name || selectedRoom.veterinarian_username}
                  </h2>
                  <p className="text-sm text-gray-500">
                    {isConnected ? (
                      <span className="text-green-600">● Conectado</span>
                    ) : (
                      <span className="text-red-600">● Desconectado</span>
                    )}
                  </p>
                </div>
              </div>

              {/* Mensajes */}
              <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
                {messages.length === 0 ? (
                  <p className="text-center text-gray-500">No hay mensajes aún</p>
                ) : (
                  messages.map((msg, index) => {
                    const isMyMessage = currentUser && msg.sender === currentUser.id;
                    const showDateSeparator = index === 0 || 
                      formatDate(messages[index - 1].timestamp) !== formatDate(msg.timestamp);

                    return (
                      <div key={msg.id}>
                        {showDateSeparator && (
                          <div className="text-center my-4">
                            <span className="bg-gray-200 px-3 py-1 rounded-full text-xs text-gray-600">
                              {formatDate(msg.timestamp)}
                            </span>
                          </div>
                        )}
                        
                        <div className={`flex mb-3 ${isMyMessage ? 'justify-end' : 'justify-start'}`}>
                          <div className={`max-w-xs lg:max-w-md ${isMyMessage ? 'order-2' : 'order-1'}`}>
                            {!isMyMessage && (
                              <p className="text-xs text-gray-500 mb-1">{msg.sender_username}</p>
                            )}
                            <div
                              className={`rounded-lg p-3 ${
                                isMyMessage
                                  ? 'bg-blue-500 text-white'
                                  : 'bg-white border border-gray-200'
                              }`}
                            >
                              <p>{msg.message}</p>
                              <p className={`text-xs mt-1 ${isMyMessage ? 'text-blue-100' : 'text-gray-400'}`}>
                                {formatTime(msg.timestamp)}
                                {isMyMessage && (msg.is_read ? ' ✓✓' : ' ✓')}
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    );
                  })
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Input */}
              <form onSubmit={sendMessage} className="p-4 border-t bg-white">
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={messageText}
                    onChange={(e) => setMessageText(e.target.value)}
                    placeholder="Escribe un mensaje..."
                    className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    disabled={!isConnected}
                  />
                  <button
                    type="submit"
                    disabled={!isConnected || !messageText.trim()}
                    className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
                  >
                    Enviar
                  </button>
                </div>
              </form>
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center text-gray-500">
              <p>Selecciona una conversación para comenzar</p>
            </div>
          )}
        </div>
      </div>

      {/* Modal Nueva Conversación */}
      {showNewChatModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4">Nueva Conversación</h2>
            <form onSubmit={createNewChat}>
              <label className="block text-sm font-medium mb-2">
                Selecciona un Veterinario
              </label>
              <select
                value={selectedVet}
                onChange={(e) => setSelectedVet(e.target.value)}
                className="w-full border rounded-lg px-3 py-2 mb-4"
                required
              >
                <option value="">-- Seleccionar --</option>
                {veterinarians.map(vet => (
                  <option key={vet.id} value={vet.id}>
                    {vet.first_name && vet.last_name
                      ? `${vet.first_name} ${vet.last_name}`
                      : vet.username}
                  </option>
                ))}
              </select>
              
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => {
                    setShowNewChatModal(false);
                    setSelectedVet('');
                  }}
                  className="flex-1 bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="flex-1 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
                >
                  Crear
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chat;
