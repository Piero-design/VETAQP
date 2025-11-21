import { useState, useEffect } from 'react';
import axios from 'axios';

const Memberships = () => {
  const [memberships, setMemberships] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [filterStatus, setFilterStatus] = useState('');
  
  const [formData, setFormData] = useState({
    plan_name: 'BASIC',
    price: '',
    auto_renew: false,
    duration_days: 30,
    notes: ''
  });

  const plans = [
    { 
      name: 'BASIC', 
      label: 'Básico', 
      price: 49.90, 
      duration: 30,
      benefits: ['10% descuento en consultas', 'Recordatorios de vacunas', 'Soporte básico']
    },
    { 
      name: 'PREMIUM', 
      label: 'Premium', 
      price: 99.90, 
      duration: 30,
      benefits: ['20% descuento en consultas', 'Descuento en productos', 'Prioridad en citas', 'Soporte 24/7']
    },
    { 
      name: 'VIP', 
      label: 'VIP', 
      price: 149.90, 
      duration: 30,
      benefits: ['30% descuento en consultas', '15% descuento en productos', 'Citas prioritarias', 'Consultas virtuales gratis', 'Soporte premium']
    }
  ];

  useEffect(() => {
    loadMemberships();
  }, [filterStatus]);

  const loadMemberships = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('access_token');
      
      let url = '/api/memberships/';
      if (filterStatus) url += `?status=${filterStatus}`;
      
      const response = await axios.get(url, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setMemberships(response.data);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al cargar membresías');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePlanSelect = (plan) => {
    setFormData({
      ...formData,
      plan_name: plan.name,
      price: plan.price.toString(),
      duration_days: plan.duration
    });
    setShowForm(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('access_token');
      await axios.post('/api/memberships/', formData, {
        headers: { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      setFormData({ plan_name: 'BASIC', price: '', auto_renew: false, duration_days: 30, notes: '' });
      setShowForm(false);
      loadMemberships();
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al crear membresía');
    }
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      'ACTIVE': { label: 'Activo', color: 'bg-green-100 text-green-800' },
      'EXPIRED': { label: 'Expirado', color: 'bg-red-100 text-red-800' },
      'CANCELLED': { label: 'Cancelado', color: 'bg-gray-100 text-gray-800' }
    };
    return statusConfig[status] || { label: status, color: 'bg-gray-100 text-gray-800' };
  };

  const getPlanBadge = (plan) => {
    const planConfig = {
      'BASIC': { color: 'bg-blue-500' },
      'PREMIUM': { color: 'bg-purple-500' },
      'VIP': { color: 'bg-yellow-500' }
    };
    return planConfig[plan] || { color: 'bg-gray-500' };
  };

  const activeMembership = memberships.find(m => m.status === 'ACTIVE');

  if (loading && memberships.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Cargando membresías...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Membresías</h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {/* Membresía activa actual */}
      {activeMembership && (
        <div className={`${getPlanBadge(activeMembership.plan_name).color} text-white shadow-lg rounded-lg p-6 mb-6`}>
          <div className="flex justify-between items-start">
            <div>
              <h2 className="text-2xl font-bold mb-2">Plan {activeMembership.plan_name_display}</h2>
              <p className="text-lg mb-4">Tu membresía activa</p>
              <div className="space-y-2">
                <p className="flex items-center gap-2">
                  <span className="font-semibold">Vence:</span> 
                  {new Date(activeMembership.end_date).toLocaleDateString('es-PE')}
                </p>
                <p className="flex items-center gap-2">
                  <span className="font-semibold">Días restantes:</span> 
                  {activeMembership.days_remaining} días
                </p>
                <p className="flex items-center gap-2">
                  <span className="font-semibold">Renovación automática:</span> 
                  {activeMembership.auto_renew ? '✓ Activada' : '✗ Desactivada'}
                </p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold">S/. {activeMembership.price}</div>
              <div className="text-sm opacity-90">/ mes</div>
            </div>
          </div>
        </div>
      )}

      {/* Planes disponibles */}
      {!showForm && !activeMembership && (
        <div className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Planes Disponibles</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {plans.map((plan) => (
              <div key={plan.name} className="bg-white shadow-lg rounded-lg overflow-hidden border-2 border-gray-200 hover:border-blue-500 transition">
                <div className={`${getPlanBadge(plan.name).color} text-white p-6`}>
                  <h3 className="text-2xl font-bold mb-2">{plan.label}</h3>
                  <div className="text-4xl font-bold mb-1">S/. {plan.price}</div>
                  <div className="text-sm opacity-90">/ {plan.duration} días</div>
                </div>
                <div className="p-6">
                  <ul className="space-y-3 mb-6">
                    {plan.benefits.map((benefit, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-green-600 font-bold">✓</span>
                        <span className="text-gray-700">{benefit}</span>
                      </li>
                    ))}
                  </ul>
                  <button
                    onClick={() => handlePlanSelect(plan)}
                    className="w-full bg-blue-600 text-white px-4 py-3 rounded-lg hover:bg-blue-700 font-semibold"
                  >
                    Suscribirme
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Formulario de suscripción */}
      {showForm && (
        <div className="bg-white shadow-md rounded-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Confirmar Suscripción</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Plan Seleccionado
              </label>
              <input
                type="text"
                value={plans.find(p => p.name === formData.plan_name)?.label || formData.plan_name}
                disabled
                className="w-full border border-gray-300 rounded-lg px-3 py-2 bg-gray-100"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Precio (S/.)
              </label>
              <input
                type="number"
                step="0.01"
                value={formData.price}
                onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Duración (días)
              </label>
              <input
                type="number"
                min="1"
                value={formData.duration_days}
                onChange={(e) => setFormData({ ...formData, duration_days: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
                required
              />
            </div>

            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="auto_renew"
                checked={formData.auto_renew}
                onChange={(e) => setFormData({ ...formData, auto_renew: e.target.checked })}
                className="w-4 h-4"
              />
              <label htmlFor="auto_renew" className="text-sm text-gray-700">
                Activar renovación automática
              </label>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Notas (opcional)
              </label>
              <textarea
                value={formData.notes}
                onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
                rows="3"
              />
            </div>

            <div className="flex gap-3">
              <button
                type="submit"
                className="flex-1 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
              >
                Confirmar Suscripción
              </button>
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="flex-1 bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400"
              >
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Filtros */}
      <div className="bg-white shadow-md rounded-lg p-4 mb-6">
        <h3 className="text-lg font-semibold mb-3">Filtrar Historial</h3>
        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
          className="w-full md:w-64 border border-gray-300 rounded-lg px-3 py-2"
        >
          <option value="">Todos los estados</option>
          <option value="ACTIVE">Activo</option>
          <option value="EXPIRED">Expirado</option>
          <option value="CANCELLED">Cancelado</option>
        </select>
      </div>

      {/* Historial de membresías */}
      <div className="bg-white shadow-md rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Historial de Membresías</h2>
        {memberships.length === 0 ? (
          <p className="text-gray-500">No tienes membresías registradas</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Plan</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Inicio</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fin</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Precio</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Días Restantes</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Auto-renovación</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {memberships.map((membership) => {
                  const statusInfo = getStatusBadge(membership.status);
                  return (
                    <tr key={membership.id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900">
                        {membership.plan_name_display}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${statusInfo.color}`}>
                          {statusInfo.label}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(membership.start_date).toLocaleDateString('es-PE')}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(membership.end_date).toLocaleDateString('es-PE')}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">
                        S/. {membership.price}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {membership.days_remaining > 0 ? `${membership.days_remaining} días` : '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {membership.auto_renew ? '✓ Sí' : '✗ No'}
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

export default Memberships;
