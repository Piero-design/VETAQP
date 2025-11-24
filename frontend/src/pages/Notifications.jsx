import { useState, useEffect } from 'react';
import axios from 'axios';

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [filterRead, setFilterRead] = useState('');
  const [filterType, setFilterType] = useState('');
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    fetchNotifications();
    fetchUnreadCount();
  }, [filterRead, filterType]);

  const fetchNotifications = async () => {
    try {
      const token = localStorage.getItem('token');
      let url = 'http://localhost:8000/api/notifications/';
      
      const params = [];
      if (filterRead) params.push(`is_read=${filterRead}`);
      if (filterType) params.push(`notification_type=${filterType}`);
      
      if (params.length > 0) {
        url += '?' + params.join('&');
      }
      
      const response = await axios.get(url, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setNotifications(response.data);
    } catch (error) {
      console.error('Error al cargar notificaciones:', error);
    }
  };

  const fetchUnreadCount = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/api/notifications/unread-count/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUnreadCount(response.data.unread_count);
    } catch (error) {
      console.error('Error al obtener conteo:', error);
    }
  };

  const markAsRead = async (id) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`http://localhost:8000/api/notifications/${id}/mark-as-read/`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchNotifications();
      fetchUnreadCount();
    } catch (error) {
      console.error('Error al marcar como leída:', error);
    }
  };

  const markAllAsRead = async () => {
    try {
      const token = localStorage.getItem('token');
      await axios.post('http://localhost:8000/api/notifications/mark-all-as-read/', {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchNotifications();
      fetchUnreadCount();
      alert('Todas las notificaciones marcadas como leídas');
    } catch (error) {
      console.error('Error al marcar todas como leídas:', error);
    }
  };

  const deleteNotification = async (id) => {
    if (!confirm('¿Eliminar esta notificación?')) return;

    try {
      const token = localStorage.getItem('token');
      await axios.delete(`http://localhost:8000/api/notifications/${id}/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchNotifications();
      fetchUnreadCount();
    } catch (error) {
      console.error('Error al eliminar:', error);
    }
  };

  const getTypeIcon = (type) => {
    const icons = {
      INFO: 'ℹ️',
      SUCCESS: '✅',
      WARNING: '⚠️',
      ERROR: '❌'
    };
    return icons[type] || 'ℹ️';
  };

  const getTypeBadge = (type) => {
    const badges = {
      INFO: 'bg-blue-100 text-blue-800',
      SUCCESS: 'bg-green-100 text-green-800',
      WARNING: 'bg-yellow-100 text-yellow-800',
      ERROR: 'bg-red-100 text-red-800'
    };
    return badges[type] || 'bg-gray-100 text-gray-800';
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Ahora mismo';
    if (diffMins < 60) return `Hace ${diffMins} min`;
    if (diffHours < 24) return `Hace ${diffHours}h`;
    if (diffDays < 7) return `Hace ${diffDays}d`;

    return date.toLocaleDateString('es-ES', {
      day: 'numeric',
      month: 'short',
      year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
    });
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold">Centro de Notificaciones</h1>
          {unreadCount > 0 && (
            <p className="text-gray-600 mt-1">
              Tienes <span className="font-bold text-blue-600">{unreadCount}</span> notificación{unreadCount !== 1 ? 'es' : ''} sin leer
            </p>
          )}
        </div>
        {unreadCount > 0 && (
          <button
            onClick={markAllAsRead}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            ✓ Marcar todas como leídas
          </button>
        )}
      </div>

      {/* Filtros */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <h2 className="text-lg font-bold mb-3">Filtros</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">Estado de Lectura</label>
            <select
              value={filterRead}
              onChange={(e) => setFilterRead(e.target.value)}
              className="w-full border rounded p-2"
            >
              <option value="">Todas</option>
              <option value="false">No leídas</option>
              <option value="true">Leídas</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Tipo</label>
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="w-full border rounded p-2"
            >
              <option value="">Todos los tipos</option>
              <option value="INFO">Información</option>
              <option value="SUCCESS">Éxito</option>
              <option value="WARNING">Advertencia</option>
              <option value="ERROR">Error</option>
            </select>
          </div>
        </div>
      </div>

      {/* Lista de Notificaciones */}
      <div className="space-y-3">
        {notifications.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-8 text-center">
            <p className="text-gray-500 text-lg">📭 No hay notificaciones</p>
          </div>
        ) : (
          notifications.map(notif => (
            <div
              key={notif.id}
              className={`bg-white rounded-lg shadow-md p-4 transition hover:shadow-lg ${
                !notif.is_read ? 'border-l-4 border-blue-500' : ''
              }`}
            >
              <div className="flex items-start gap-4">
                {/* Icono del tipo */}
                <div className="text-3xl flex-shrink-0 mt-1">
                  {getTypeIcon(notif.notification_type)}
                </div>

                {/* Contenido */}
                <div className="flex-1">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h3 className={`font-bold text-lg ${!notif.is_read ? 'text-gray-900' : 'text-gray-600'}`}>
                        {notif.title}
                        {!notif.is_read && <span className="ml-2 text-blue-500">•</span>}
                      </h3>
                      <p className={`text-sm ${!notif.is_read ? 'text-gray-700' : 'text-gray-500'}`}>
                        {notif.message}
                      </p>
                    </div>
                    <span className={`px-2 py-1 rounded text-xs font-semibold whitespace-nowrap ml-2 ${getTypeBadge(notif.notification_type)}`}>
                      {notif.notification_type_display}
                    </span>
                  </div>

                  <div className="flex justify-between items-center mt-3">
                    <span className="text-xs text-gray-500">
                      {formatDate(notif.created_at)}
                    </span>
                    <div className="flex gap-2">
                      {!notif.is_read && (
                        <button
                          onClick={() => markAsRead(notif.id)}
                          className="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded hover:bg-blue-200"
                        >
                          ✓ Marcar como leída
                        </button>
                      )}
                      <button
                        onClick={() => deleteNotification(notif.id)}
                        className="text-xs bg-red-100 text-red-700 px-3 py-1 rounded hover:bg-red-200"
                      >
                        🗑️ Eliminar
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Resumen */}
      {notifications.length > 0 && (
        <div className="mt-6 bg-gray-50 rounded-lg p-4 text-center text-sm text-gray-600">
          Mostrando {notifications.length} notificación{notifications.length !== 1 ? 'es' : ''}
        </div>
      )}
    </div>
  );
};

export default Notifications;
