import { useState, useEffect } from 'react';
import { listOrders } from '../api/orderService';
import { toast } from 'react-toastify';

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState('');

  useEffect(() => {
    fetchOrders();
  }, [filterStatus]);

  const fetchOrders = async () => {
    setLoading(true);
    try {
      const response = await listOrders();
      let filtered = response.data;
      
      if (filterStatus) {
        filtered = filtered.filter(order => order.status === filterStatus);
      }
      
      setOrders(filtered);
    } catch (error) {
      toast.error('Error al cargar pedidos');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      pending: 'bg-yellow-100 text-yellow-800',
      confirmed: 'bg-blue-100 text-blue-800',
      processing: 'bg-blue-100 text-blue-800',
      shipped: 'bg-purple-100 text-purple-800',
      delivered: 'bg-green-100 text-green-800',
      cancelled: 'bg-red-100 text-red-800',
      returned: 'bg-orange-100 text-orange-800'
    };
    return badges[status] || 'bg-gray-100 text-gray-800';
  };

  const getStatusLabel = (status) => {
    const labels = {
      pending: 'Pendiente',
      confirmed: 'Confirmado',
      processing: 'En Proceso',
      shipped: 'Enviado',
      delivered: 'Entregado',
      cancelled: 'Cancelado',
      returned: 'Devuelto'
    };
    return labels[status] || status;
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Mis Pedidos</h1>

      <div className="card p-4">
        <label className="block text-sm font-semibold mb-2">Filtrar por estado:</label>
        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
          className="input w-full md:w-64"
        >
          <option value="">Todos</option>
          <option value="pending">Pendiente</option>
          <option value="confirmed">Confirmado</option>
          <option value="processing">En Proceso</option>
          <option value="shipped">Enviado</option>
          <option value="delivered">Entregado</option>
          <option value="cancelled">Cancelado</option>
        </select>
      </div>

      {loading ? (
        <div className="text-center py-8">Cargando pedidos...</div>
      ) : orders.length === 0 ? (
        <div className="card p-6 text-center">
          <p className="text-gray-500 mb-4">No hay pedidos registrados</p>
          <a href="/" className="btn-primary">
            Ir al catálogo
          </a>
        </div>
      ) : (
        <div className="space-y-4">
          {orders.map(order => (
            <div key={order.id} className="card p-4 hover:shadow-lg transition">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3 className="font-bold text-lg">{order.order_number}</h3>
                  <p className="text-sm text-gray-600">
                    {new Date(order.created_at).toLocaleDateString('es-ES', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </p>
                </div>
                <div className="text-right">
                  <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${getStatusBadge(order.status)}`}>
                    {getStatusLabel(order.status)}
                  </span>
                  <p className="text-2xl font-bold text-green-600 mt-2">S/ {Number(order.total).toFixed(2)}</p>
                </div>
              </div>

              <div className="border-t pt-3">
                <h4 className="font-semibold mb-2">Items:</h4>
                <div className="space-y-2">
                  {order.items.map(item => (
                    <div key={item.id} className="flex justify-between items-center text-sm">
                      <div>
                        <span className="font-semibold">{item.product.name}</span>
                        <span className="text-gray-600"> x{item.quantity}</span>
                      </div>
                      <p className="font-bold">S/ {(Number(item.price) * item.quantity).toFixed(2)}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="border-t mt-3 pt-3 text-sm">
                <div className="flex justify-between">
                  <span>Envío a:</span>
                  <span className="font-semibold">{order.shipping_city}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Orders;
