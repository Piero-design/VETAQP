import { useState, useEffect } from 'react';
import axios from 'axios';

const Payments = () => {
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [filterStatus, setFilterStatus] = useState('');
  const [filterMethod, setFilterMethod] = useState('');
  
  const [formData, setFormData] = useState({
    amount: '',
    payment_method: 'CARD',
    transaction_id: '',
    notes: ''
  });

  useEffect(() => {
    loadPayments();
  }, [filterStatus, filterMethod]);

  const loadPayments = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('access_token');
      
      let url = '/api/payments/';
      const params = new URLSearchParams();
      if (filterStatus) params.append('status', filterStatus);
      if (filterMethod) params.append('payment_method', filterMethod);
      if (params.toString()) url += '?' + params.toString();
      
      const response = await axios.get(url, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setPayments(response.data);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al cargar pagos');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('access_token');
      await axios.post('/api/payments/', formData, {
        headers: { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      setFormData({ amount: '', payment_method: 'CARD', transaction_id: '', notes: '' });
      setShowForm(false);
      loadPayments();
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al crear pago');
    }
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      'PENDING': { label: 'Pendiente', color: 'bg-yellow-100 text-yellow-800' },
      'COMPLETED': { label: 'Completado', color: 'bg-green-100 text-green-800' },
      'FAILED': { label: 'Fallido', color: 'bg-red-100 text-red-800' },
      'REFUNDED': { label: 'Reembolsado', color: 'bg-blue-100 text-blue-800' }
    };
    return statusConfig[status] || { label: status, color: 'bg-gray-100 text-gray-800' };
  };

  const getMethodIcon = (method) => {
    const icons = {
      'CASH': '💵',
      'CARD': '💳',
      'TRANSFER': '🏦',
      'YAPE': '📱'
    };
    return icons[method] || '💰';
  };

  if (loading && payments.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Cargando pagos...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Gestión de Pagos</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          {showForm ? 'Cancelar' : '+ Registrar Pago'}
        </button>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {/* Formulario para registrar pago */}
      {showForm && (
        <div className="bg-white shadow-md rounded-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Registrar Nuevo Pago</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Monto (S/.)
              </label>
              <input
                type="number"
                step="0.01"
                min="0.01"
                value={formData.amount}
                onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
                placeholder="150.00"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Método de Pago
              </label>
              <select
                value={formData.payment_method}
                onChange={(e) => setFormData({ ...formData, payment_method: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
                required
              >
                <option value="CARD">💳 Tarjeta</option>
                <option value="CASH">💵 Efectivo</option>
                <option value="TRANSFER">🏦 Transferencia Bancaria</option>
                <option value="YAPE">📱 Yape/Plin</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                ID de Transacción (opcional)
              </label>
              <input
                type="text"
                value={formData.transaction_id}
                onChange={(e) => setFormData({ ...formData, transaction_id: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
                placeholder="TXN123456"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Notas
              </label>
              <textarea
                value={formData.notes}
                onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
                rows="3"
                placeholder="Detalles adicionales del pago..."
              />
            </div>

            <button
              type="submit"
              className="w-full bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
            >
              Registrar Pago
            </button>
          </form>
        </div>
      )}

      {/* Filtros */}
      <div className="bg-white shadow-md rounded-lg p-4 mb-6">
        <h3 className="text-lg font-semibold mb-3">Filtros</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Estado
            </label>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
            >
              <option value="">Todos</option>
              <option value="PENDING">Pendiente</option>
              <option value="COMPLETED">Completado</option>
              <option value="FAILED">Fallido</option>
              <option value="REFUNDED">Reembolsado</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Método de Pago
            </label>
            <select
              value={filterMethod}
              onChange={(e) => setFilterMethod(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2"
            >
              <option value="">Todos</option>
              <option value="CARD">Tarjeta</option>
              <option value="CASH">Efectivo</option>
              <option value="TRANSFER">Transferencia</option>
              <option value="YAPE">Yape/Plin</option>
            </select>
          </div>
        </div>
      </div>

      {/* Resumen de pagos */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white shadow-md rounded-lg p-4">
          <div className="text-sm text-gray-600">Total Pagos</div>
          <div className="text-2xl font-bold text-gray-900">{payments.length}</div>
        </div>
        <div className="bg-white shadow-md rounded-lg p-4">
          <div className="text-sm text-gray-600">Completados</div>
          <div className="text-2xl font-bold text-green-600">
            {payments.filter(p => p.status === 'COMPLETED').length}
          </div>
        </div>
        <div className="bg-white shadow-md rounded-lg p-4">
          <div className="text-sm text-gray-600">Pendientes</div>
          <div className="text-2xl font-bold text-yellow-600">
            {payments.filter(p => p.status === 'PENDING').length}
          </div>
        </div>
        <div className="bg-white shadow-md rounded-lg p-4">
          <div className="text-sm text-gray-600">Monto Total</div>
          <div className="text-2xl font-bold text-blue-600">
            S/. {payments.reduce((sum, p) => sum + parseFloat(p.amount), 0).toFixed(2)}
          </div>
        </div>
      </div>

      {/* Lista de pagos */}
      <div className="bg-white shadow-md rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Historial de Pagos</h2>
        {payments.length === 0 ? (
          <p className="text-gray-500">No hay pagos registrados</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Fecha
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Monto
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Método
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Estado
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    ID Transacción
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Notas
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {payments.map((payment) => {
                  const statusInfo = getStatusBadge(payment.status);
                  return (
                    <tr key={payment.id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(payment.created_at).toLocaleString('es-PE')}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900">
                        S/. {parseFloat(payment.amount).toFixed(2)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {getMethodIcon(payment.payment_method)} {payment.payment_method_display}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${statusInfo.color}`}>
                          {statusInfo.label}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {payment.transaction_id || '-'}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">
                        {payment.notes || '-'}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Payments;
