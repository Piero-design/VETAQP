import { useState, useEffect } from 'react';
import axios from 'axios';

function OrderTracking() {
  const [orders, setOrders] = useState([]);
  const [trackingNumber, setTrackingNumber] = useState('');
  const [trackingResult, setTrackingResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('myOrders'); // myOrders or track
  const [filterStatus, setFilterStatus] = useState('');
  const [isStaff, setIsStaff] = useState(false);
  const [showShippingModal, setShowShippingModal] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [shippingForm, setShippingForm] = useState({
    shipping_status: '',
    tracking_number: '',
    shipping_address: '',
    estimated_delivery_date: ''
  });

  useEffect(() => {
    checkUserRole();
    if (activeTab === 'myOrders') {
      fetchMyOrders();
    }
  }, [activeTab, filterStatus]);

  const checkUserRole = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) return;
      
      const response = await axios.get('http://localhost:8000/api/auth/profile/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setIsStaff(response.data.is_staff);
    } catch (error) {
      console.error('Error checking user role:', error);
    }
  };

  const fetchMyOrders = async () => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('access_token');
      const url = filterStatus 
        ? `http://localhost:8000/api/orders/my-orders/?shipping_status=${filterStatus}`
        : 'http://localhost:8000/api/orders/my-orders/';
      
      const response = await axios.get(url, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setOrders(response.data);
    } catch (error) {
      console.error('Error fetching orders:', error);
      setError('Error al cargar los pedidos');
    } finally {
      setLoading(false);
    }
  };

  const trackOrder = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setTrackingResult(null);
    
    try {
      const response = await axios.get(
        `http://localhost:8000/api/orders/tracking/${trackingNumber}/`
      );
      setTrackingResult(response.data);
    } catch (error) {
      console.error('Error tracking order:', error);
      setError('No se encontró ningún pedido con ese número de seguimiento');
    } finally {
      setLoading(false);
    }
  };

  const openShippingModal = (order) => {
    setSelectedOrder(order);
    setShippingForm({
      shipping_status: order.shipping_status || '',
      tracking_number: order.tracking_number || '',
      shipping_address: order.shipping_address || '',
      estimated_delivery_date: order.estimated_delivery_date || ''
    });
    setShowShippingModal(true);
  };

  const handleUpdateShipping = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('access_token');
      await axios.patch(
        `http://localhost:8000/api/orders/${selectedOrder.id}/shipping/`,
        shippingForm,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setShowShippingModal(false);
      fetchMyOrders();
      alert('Estado de envío actualizado correctamente');
    } catch (error) {
      console.error('Error updating shipping:', error);
      alert(error.response?.data?.tracking_number?.[0] || 'Error al actualizar el estado de envío');
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      PENDING: 'bg-gray-200 text-gray-800',
      PREPARING: 'bg-yellow-200 text-yellow-800',
      SHIPPED: 'bg-blue-200 text-blue-800',
      IN_TRANSIT: 'bg-blue-300 text-blue-900',
      OUT_FOR_DELIVERY: 'bg-purple-200 text-purple-800',
      DELIVERED: 'bg-green-200 text-green-800',
      FAILED: 'bg-red-200 text-red-800'
    };
    return colors[status] || 'bg-gray-200 text-gray-800';
  };

  const getStatusTimeline = (order) => {
    const statuses = [
      { key: 'PENDING', label: 'Pendiente', icon: '📦' },
      { key: 'PREPARING', label: 'Preparando', icon: '📋' },
      { key: 'SHIPPED', label: 'Enviado', icon: '🚚' },
      { key: 'IN_TRANSIT', label: 'En tránsito', icon: '🛣️' },
      { key: 'OUT_FOR_DELIVERY', label: 'En reparto', icon: '🚲' },
      { key: 'DELIVERED', label: 'Entregado', icon: '✅' }
    ];

    const currentIndex = statuses.findIndex(s => s.key === order.shipping_status);
    
    return statuses.map((status, index) => ({
      ...status,
      completed: index <= currentIndex,
      active: index === currentIndex
    }));
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatDateTime = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const OrderCard = ({ order, showActions = false }) => (
    <div className="bg-white rounded-lg shadow-md p-6 mb-4">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-bold">Pedido #{order.id}</h3>
          <p className="text-gray-600">Usuario: {order.user_username}</p>
          <p className="text-gray-600">Fecha: {formatDate(order.created_at)}</p>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-blue-600">${order.total}</div>
          <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold mt-2 ${getStatusColor(order.shipping_status)}`}>
            {order.shipping_status_display}
          </span>
        </div>
      </div>

      {/* Timeline */}
      <div className="mb-4">
        <div className="flex items-center justify-between relative">
          {getStatusTimeline(order).map((status, index) => (
            <div key={status.key} className="flex flex-col items-center z-10 flex-1">
              <div className={`w-12 h-12 rounded-full flex items-center justify-center text-2xl ${
                status.completed ? 'bg-blue-500 text-white' : 'bg-gray-200'
              }`}>
                {status.icon}
              </div>
              <div className={`text-xs mt-2 text-center font-medium ${
                status.active ? 'text-blue-600 font-bold' : status.completed ? 'text-gray-700' : 'text-gray-400'
              }`}>
                {status.label}
              </div>
            </div>
          ))}
          <div className="absolute top-6 left-0 right-0 h-1 bg-gray-200 -z-0" style={{ margin: '0 6%' }}>
            <div 
              className="h-full bg-blue-500 transition-all" 
              style={{ width: `${(getStatusTimeline(order).filter(s => s.completed).length - 1) / (getStatusTimeline(order).length - 1) * 100}%` }}
            />
          </div>
        </div>
      </div>

      {/* Información de envío */}
      <div className="border-t pt-4 space-y-2">
        {order.tracking_number && (
          <div className="flex justify-between">
            <span className="text-gray-600">Número de seguimiento:</span>
            <span className="font-semibold">{order.tracking_number}</span>
          </div>
        )}
        {order.shipping_address && (
          <div className="flex justify-between">
            <span className="text-gray-600">Dirección:</span>
            <span className="font-semibold text-right">{order.shipping_address}</span>
          </div>
        )}
        {order.estimated_delivery_date && (
          <div className="flex justify-between">
            <span className="text-gray-600">Entrega estimada:</span>
            <span className="font-semibold">{formatDate(order.estimated_delivery_date)}</span>
          </div>
        )}
        {order.shipped_date && (
          <div className="flex justify-between">
            <span className="text-gray-600">Fecha de envío:</span>
            <span className="font-semibold">{formatDateTime(order.shipped_date)}</span>
          </div>
        )}
        {order.delivered_date && (
          <div className="flex justify-between">
            <span className="text-gray-600">Fecha de entrega:</span>
            <span className="font-semibold">{formatDateTime(order.delivered_date)}</span>
          </div>
        )}
      </div>

      {/* Items del pedido */}
      <div className="border-t pt-4 mt-4">
        <h4 className="font-semibold mb-2">Productos:</h4>
        <div className="space-y-2">
          {order.items.map(item => (
            <div key={item.id} className="flex justify-between text-sm">
              <span>{item.product_name} x{item.quantity}</span>
              <span className="font-semibold">${item.subtotal}</span>
            </div>
          ))}
        </div>
      </div>

      {showActions && isStaff && (
        <div className="border-t pt-4 mt-4">
          <button
            onClick={() => openShippingModal(order)}
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
          >
            Actualizar Estado de Envío
          </button>
        </div>
      )}
    </div>
  );

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Seguimiento de Pedidos</h1>

      {/* Tabs */}
      <div className="flex gap-4 mb-6 border-b">
        <button
          onClick={() => setActiveTab('myOrders')}
          className={`pb-2 px-4 ${activeTab === 'myOrders' ? 'border-b-2 border-blue-600 text-blue-600 font-semibold' : 'text-gray-600'}`}
        >
          Mis Pedidos
        </button>
        <button
          onClick={() => setActiveTab('track')}
          className={`pb-2 px-4 ${activeTab === 'track' ? 'border-b-2 border-blue-600 text-blue-600 font-semibold' : 'text-gray-600'}`}
        >
          Rastrear Pedido
        </button>
      </div>

      {/* Contenido de Mis Pedidos */}
      {activeTab === 'myOrders' && (
        <div>
          {/* Filtros */}
          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">Filtrar por estado:</label>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="border rounded px-4 py-2"
            >
              <option value="">Todos</option>
              <option value="PENDING">Pendiente</option>
              <option value="PREPARING">Preparando</option>
              <option value="SHIPPED">Enviado</option>
              <option value="IN_TRANSIT">En tránsito</option>
              <option value="OUT_FOR_DELIVERY">En reparto</option>
              <option value="DELIVERED">Entregado</option>
            </select>
          </div>

          {loading ? (
            <div className="text-center py-8">Cargando pedidos...</div>
          ) : error ? (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          ) : orders.length === 0 ? (
            <div className="bg-gray-100 rounded-lg p-8 text-center">
              <p className="text-gray-600">No tienes pedidos{filterStatus ? ' con este estado' : ''}</p>
            </div>
          ) : (
            <div>
              {orders.map(order => (
                <OrderCard key={order.id} order={order} showActions={true} />
              ))}
            </div>
          )}
        </div>
      )}

      {/* Contenido de Rastrear Pedido */}
      {activeTab === 'track' && (
        <div>
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">Rastrear por Número de Seguimiento</h2>
            <form onSubmit={trackOrder} className="flex gap-4">
              <input
                type="text"
                value={trackingNumber}
                onChange={(e) => setTrackingNumber(e.target.value)}
                placeholder="Ingresa tu número de seguimiento"
                className="flex-1 border rounded px-4 py-2"
                required
              />
              <button
                type="submit"
                disabled={loading}
                className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
              >
                {loading ? 'Buscando...' : 'Rastrear'}
              </button>
            </form>
          </div>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
              {error}
            </div>
          )}

          {trackingResult && (
            <OrderCard order={trackingResult} showActions={false} />
          )}
        </div>
      )}

      {/* Modal para actualizar envío */}
      {showShippingModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full">
            <h2 className="text-2xl font-bold mb-4">Actualizar Estado de Envío</h2>
            <form onSubmit={handleUpdateShipping} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Estado de Envío</label>
                <select
                  value={shippingForm.shipping_status}
                  onChange={(e) => setShippingForm({...shippingForm, shipping_status: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                  required
                >
                  <option value="">Seleccionar...</option>
                  <option value="PENDING">Pendiente</option>
                  <option value="PREPARING">Preparando</option>
                  <option value="SHIPPED">Enviado</option>
                  <option value="IN_TRANSIT">En tránsito</option>
                  <option value="OUT_FOR_DELIVERY">En reparto</option>
                  <option value="DELIVERED">Entregado</option>
                  <option value="FAILED">Fallo en entrega</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Número de Seguimiento</label>
                <input
                  type="text"
                  value={shippingForm.tracking_number}
                  onChange={(e) => setShippingForm({...shippingForm, tracking_number: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Dirección de Envío</label>
                <textarea
                  value={shippingForm.shipping_address}
                  onChange={(e) => setShippingForm({...shippingForm, shipping_address: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                  rows="2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Fecha Estimada de Entrega</label>
                <input
                  type="date"
                  value={shippingForm.estimated_delivery_date}
                  onChange={(e) => setShippingForm({...shippingForm, estimated_delivery_date: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                />
              </div>
              <div className="flex gap-2 justify-end">
                <button
                  type="button"
                  onClick={() => setShowShippingModal(false)}
                  className="px-4 py-2 border rounded hover:bg-gray-100"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Actualizar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default OrderTracking;
