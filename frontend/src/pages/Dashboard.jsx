import { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [salesData, setSalesData] = useState(null);
  const [popularProducts, setPopularProducts] = useState([]);
  const [appointmentsStats, setAppointmentsStats] = useState(null);
  const [recentActivity, setRecentActivity] = useState([]);
  const [lowStock, setLowStock] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [period, setPeriod] = useState('daily');
  const [isStaff, setIsStaff] = useState(false);

  useEffect(() => {
    checkStaffAccess();
  }, []);

  useEffect(() => {
    if (isStaff) {
      fetchAllData();
    }
  }, [isStaff, period]);

  const checkStaffAccess = async () => {
    try {
      const token = localStorage.getItem('access');
      if (!token) {
        setError('Debes iniciar sesión');
        setLoading(false);
        return;
      }

      // Intentar acceder al endpoint de stats para verificar permisos
      const response = await axios.get('http://localhost:8000/api/dashboard/stats/', {
        headers: { Authorization: `Bearer ${token}` }
      });

      // Si llegamos aquí, el usuario tiene permisos de staff
      setIsStaff(true);
    } catch (error) {
      console.error('Error checking staff access:', error);
      if (error.response?.status === 403) {
        setError('No tienes permisos para acceder al dashboard. Solo usuarios administradores pueden ver esta página.');
      } else if (error.response?.status === 401) {
        setError('Tu sesión ha expirado. Por favor, inicia sesión nuevamente.');
      } else {
        setError('Error al verificar permisos. Verifica que estés logueado como administrador.');
      }
      setLoading(false);
    }
  };

  const fetchAllData = async () => {
    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('access');
      const config = {
        headers: { Authorization: `Bearer ${token}` }
      };

      const [
        statsRes,
        salesRes,
        productsRes,
        appointmentsRes,
        activityRes,
        stockRes
      ] = await Promise.all([
        axios.get('http://localhost:8000/api/dashboard/stats/', config),
        axios.get(`http://localhost:8000/api/dashboard/sales-over-time/?period=${period}`, config),
        axios.get('http://localhost:8000/api/dashboard/popular-products/?limit=5', config),
        axios.get('http://localhost:8000/api/dashboard/appointments-stats/', config),
        axios.get('http://localhost:8000/api/dashboard/recent-activity/?limit=10', config),
        axios.get('http://localhost:8000/api/dashboard/low-stock/?threshold=10', config)
      ]);

      setStats(statsRes.data);
      setSalesData(salesRes.data);
      setPopularProducts(productsRes.data.products);
      setAppointmentsStats(appointmentsRes.data);
      setRecentActivity(activityRes.data.activities);
      setLowStock(stockRes.data.products);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setError('Error al cargar los datos del dashboard');
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ title, value, subtitle, icon, color = 'blue' }) => (
    <div className={`bg-white rounded-lg shadow p-6 border-l-4 border-${color}-500`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-600 text-sm font-medium">{title}</p>
          <p className="text-3xl font-bold mt-2">{value}</p>
          {subtitle && <p className="text-gray-500 text-sm mt-1">{subtitle}</p>}
        </div>
        <div className={`text-4xl text-${color}-500`}>{icon}</div>
      </div>
    </div>
  );

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('es-PE', {
      style: 'currency',
      currency: 'PEN'
    }).format(value);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    });
  };

  const getActivityIcon = (type) => {
    return type === 'order' ? '🛒' : '📅';
  };

  const getStatusColor = (status) => {
    const colors = {
      PENDING: 'bg-yellow-100 text-yellow-800',
      PROCESSING: 'bg-blue-100 text-blue-800',
      COMPLETED: 'bg-green-100 text-green-800',
      SCHEDULED: 'bg-purple-100 text-purple-800',
      CONFIRMED: 'bg-green-100 text-green-800',
      CANCELLED: 'bg-red-100 text-red-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  if (loading && !stats) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center py-12">
          <div className="text-2xl">Cargando dashboard...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      </div>
    );
  }

  if (!isStaff) {
    return null;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Dashboard de Administración</h1>
        <p className="text-gray-600">Panel de control y estadísticas generales</p>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Pedidos"
          value={stats?.overview.total_orders || 0}
          subtitle={`Mes actual: ${stats?.current_month.orders || 0}`}
          icon="🛒"
          color="blue"
        />
        <StatCard
          title="Ingresos Totales"
          value={formatCurrency(stats?.overview.total_revenue || 0)}
          subtitle={`Mes actual: ${formatCurrency(stats?.current_month.revenue || 0)}`}
          icon="💰"
          color="green"
        />
        <StatCard
          title="Usuarios Activos"
          value={stats?.overview.active_users || 0}
          subtitle={`${stats?.overview.total_pets || 0} mascotas registradas`}
          icon="👥"
          color="purple"
        />
        <StatCard
          title="Citas Pendientes"
          value={stats?.overview.pending_appointments || 0}
          subtitle={`Total: ${stats?.overview.total_appointments || 0}`}
          icon="📅"
          color="orange"
        />
      </div>

      {/* Secondary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <StatCard
          title="Productos"
          value={stats?.overview.total_products || 0}
          subtitle={`${stats?.overview.low_stock_products || 0} con stock bajo`}
          icon="📦"
          color="indigo"
        />
        <StatCard
          title="Pagos Exitosos"
          value={stats?.payments.successful || 0}
          subtitle={`Total: ${formatCurrency(stats?.payments.total_amount || 0)}`}
          icon="💳"
          color="teal"
        />
        <StatCard
          title="Tasa de Éxito"
          value={stats?.payments.total > 0
            ? `${Math.round((stats.payments.successful / stats.payments.total) * 100)}%`
            : '0%'}
          subtitle={`${stats?.payments.total || 0} pagos totales`}
          icon="📊"
          color="pink"
        />
      </div>

      {/* Sales Over Time */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Ventas a lo Largo del Tiempo</h2>
          <select
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
            className="border rounded px-3 py-2"
          >
            <option value="daily">Diario</option>
            <option value="weekly">Semanal</option>
            <option value="monthly">Mensual</option>
          </select>
        </div>
        {salesData && salesData.data.length > 0 ? (
          <div className="space-y-2">
            {salesData.data.slice(-10).map((item, index) => (
              <div key={index} className="flex items-center justify-between py-2 border-b">
                <span className="text-sm text-gray-600">{formatDate(item.date)}</span>
                <div className="flex gap-4">
                  <span className="text-sm font-semibold">{item.orders} pedidos</span>
                  <span className="text-sm font-semibold text-green-600">
                    {formatCurrency(item.revenue)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-center py-8">No hay datos de ventas</p>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Popular Products */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">Productos Más Vendidos</h2>
          {popularProducts.length > 0 ? (
            <div className="space-y-3">
              {popularProducts.map((product, index) => (
                <div key={product.product_id} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl font-bold text-gray-300">#{index + 1}</span>
                    <div>
                      <div className="font-semibold">{product.product_name}</div>
                      <div className="text-sm text-gray-600">
                        {product.quantity_sold} unidades vendidas
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-bold text-green-600">{formatCurrency(product.revenue)}</div>
                    <div className="text-xs text-gray-500">{product.times_ordered} pedidos</div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-8">No hay productos vendidos</p>
          )}
        </div>

        {/* Low Stock Products */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">Productos con Stock Bajo</h2>
          {lowStock.length > 0 ? (
            <div className="space-y-3">
              {lowStock.slice(0, 5).map(product => (
                <div key={product.id} className="flex items-center justify-between p-3 bg-red-50 rounded">
                  <div>
                    <div className="font-semibold">{product.name}</div>
                    <div className="text-sm text-gray-600">{formatCurrency(product.price)}</div>
                  </div>
                  <div className="text-right">
                    <span className="text-red-600 font-bold text-lg">{product.stock}</span>
                    <div className="text-xs text-gray-500">unidades</div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-8">✅ Todos los productos tienen stock suficiente</p>
          )}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4">Actividad Reciente</h2>
        {recentActivity.length > 0 ? (
          <div className="space-y-3">
            {recentActivity.map((activity, index) => (
              <div key={index} className="flex items-center justify-between p-3 border-b last:border-b-0">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{getActivityIcon(activity.type)}</span>
                  <div>
                    <div className="font-semibold">
                      {activity.type === 'order' ? `Pedido #${activity.id}` : `Cita #${activity.id}`}
                    </div>
                    <div className="text-sm text-gray-600">
                      {activity.user} 
                      {activity.pet && ` - ${activity.pet}`}
                      {activity.amount && ` - ${formatCurrency(activity.amount)}`}
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <span className={`inline-block px-2 py-1 text-xs rounded ${getStatusColor(activity.status)}`}>
                    {activity.status}
                  </span>
                  <div className="text-xs text-gray-500 mt-1">
                    {formatDate(activity.timestamp)}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-center py-8">No hay actividad reciente</p>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
