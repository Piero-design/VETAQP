import { useState, useEffect } from 'react';
import axios from 'axios';

const Inventory = () => {
  const [movements, setMovements] = useState([]);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  
  const [formData, setFormData] = useState({
    product: '',
    movement_type: 'IN',
    quantity: '',
    reason: ''
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('access_token');
      
      const [movementsRes, productsRes] = await Promise.all([
        axios.get('/api/inventory/movements/', {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get('/api/products/')
      ]);
      
      setMovements(movementsRes.data);
      setProducts(productsRes.data);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al cargar datos');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('access_token');
      await axios.post('/api/inventory/movements/', formData, {
        headers: { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      setFormData({ product: '', movement_type: 'IN', quantity: '', reason: '' });
      setShowForm(false);
      loadData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al crear movimiento');
    }
  };

  const getMovementTypeLabel = (type) => {
    const types = {
      'IN': { label: 'Entrada', color: 'bg-green-100 text-green-800' },
      'OUT': { label: 'Salida', color: 'bg-red-100 text-red-800' },
      'ADJUSTMENT': { label: 'Ajuste', color: 'bg-blue-100 text-blue-800' }
    };
    return types[type] || { label: type, color: 'bg-gray-100 text-gray-800' };
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Cargando...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Gestión de Inventario</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          {showForm ? 'Cancelar' : '+ Nuevo Movimiento'}
        </button>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {/* Formulario para crear movimiento */}
      {showForm && (
        <div className="bg-white shadow-md rounded-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Registrar Movimiento</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Producto
              </label>
              <select
                value={formData.product}
                onChange={(e) => setFormData({ ...formData, product: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
                required
              >
                <option value="">Seleccionar producto...</option>
                {products.map((product) => (
                  <option key={product.id} value={product.id}>
                    {product.name} (Stock actual: {product.stock})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tipo de Movimiento
              </label>
              <select
                value={formData.movement_type}
                onChange={(e) => setFormData({ ...formData, movement_type: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
                required
              >
                <option value="IN">Entrada (añadir stock)</option>
                <option value="OUT">Salida (restar stock)</option>
                <option value="ADJUSTMENT">Ajuste (establecer stock exacto)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Cantidad
              </label>
              <input
                type="number"
                min="1"
                value={formData.quantity}
                onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Razón
              </label>
              <textarea
                value={formData.reason}
                onChange={(e) => setFormData({ ...formData, reason: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-3 py-2"
                rows="3"
                required
              />
            </div>

            <button
              type="submit"
              className="w-full bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
            >
              Registrar Movimiento
            </button>
          </form>
        </div>
      )}

      {/* Lista de productos con stock */}
      <div className="bg-white shadow-md rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Stock Actual</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {products.map((product) => (
            <div key={product.id} className="border border-gray-200 rounded-lg p-4">
              <h3 className="font-semibold text-lg">{product.name}</h3>
              <p className="text-sm text-gray-600 mb-2">{product.description}</p>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-500">Stock:</span>
                <span className={`font-bold text-lg ${product.stock < 10 ? 'text-red-600' : 'text-green-600'}`}>
                  {product.stock}
                </span>
              </div>
              <div className="text-sm text-gray-500 mt-1">
                Precio: S/. {product.price}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Historial de movimientos */}
      <div className="bg-white shadow-md rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Historial de Movimientos</h2>
        {movements.length === 0 ? (
          <p className="text-gray-500">No hay movimientos registrados</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Fecha
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Producto
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Tipo
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Cantidad
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Razón
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Usuario
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {movements.map((movement) => {
                  const typeInfo = getMovementTypeLabel(movement.movement_type);
                  return (
                    <tr key={movement.id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(movement.created_at).toLocaleString('es-PE')}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {movement.product_detail?.name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${typeInfo.color}`}>
                          {typeInfo.label}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {movement.quantity}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500">
                        {movement.reason}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {movement.user_username}
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

export default Inventory;
