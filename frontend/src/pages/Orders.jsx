import { useState, useEffect } from 'react';
import axios from 'axios';

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [notes, setNotes] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [loading, setLoading] = useState(false);
  const [showCart, setShowCart] = useState(false);

  useEffect(() => {
    fetchOrders();
    fetchProducts();
  }, [filterStatus]);

  const fetchOrders = async () => {
    try {
      const token = localStorage.getItem('access');
      const url = filterStatus 
        ? `http://localhost:8000/api/orders/?status=${filterStatus}`
        : 'http://localhost:8000/api/orders/';
      
      const response = await axios.get(url, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setOrders(response.data);
    } catch (error) {
      console.error('Error al cargar pedidos:', error);
    }
  };

  const fetchProducts = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/products/');
      setProducts(response.data);
    } catch (error) {
      console.error('Error al cargar productos:', error);
    }
  };

  const addToCart = (product) => {
    const existingItem = cart.find(item => item.product_id === product.id);
    
    if (existingItem) {
      setCart(cart.map(item =>
        item.product_id === product.id
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ));
    } else {
      setCart([...cart, {
        product_id: product.id,
        product_name: product.name,
        product_price: product.price,
        quantity: 1,
        stock: product.stock
      }]);
    }
    setShowCart(true);
  };

  const removeFromCart = (product_id) => {
    setCart(cart.filter(item => item.product_id !== product_id));
  };

  const updateCartQuantity = (product_id, newQuantity) => {
    if (newQuantity <= 0) {
      removeFromCart(product_id);
      return;
    }
    setCart(cart.map(item =>
      item.product_id === product_id
        ? { ...item, quantity: newQuantity }
        : item
    ));
  };

  const calculateTotal = () => {
    return cart.reduce((sum, item) => sum + (item.product_price * item.quantity), 0).toFixed(2);
  };

  const createOrder = async (e) => {
    e.preventDefault();
    if (cart.length === 0) {
      alert('El carrito está vacío');
      return;
    }

    setLoading(true);
    try {
      const token = localStorage.getItem('access');
      const orderData = {
        notes,
        items_data: cart.map(item => ({
          product_id: item.product_id,
          quantity: item.quantity
        }))
      };

      await axios.post('http://localhost:8000/api/orders/', orderData, {
        headers: { Authorization: `Bearer ${token}` }
      });

      alert('Pedido creado exitosamente');
      setCart([]);
      setNotes('');
      setShowCart(false);
      fetchOrders();
      fetchProducts(); // Actualizar stock
    } catch (error) {
      console.error('Error al crear pedido:', error);
      alert(error.response?.data?.items?.[0] || 'Error al crear el pedido');
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      PENDING: 'bg-yellow-100 text-yellow-800',
      PROCESSING: 'bg-blue-100 text-blue-800',
      COMPLETED: 'bg-green-100 text-green-800',
      CANCELLED: 'bg-red-100 text-red-800'
    };
    return badges[status] || 'bg-gray-100 text-gray-800';
  };

  const getStatusLabel = (status) => {
    const labels = {
      PENDING: 'Pendiente',
      PROCESSING: 'En Proceso',
      COMPLETED: 'Completado',
      CANCELLED: 'Cancelado'
    };
    return labels[status] || status;
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Gestión de Pedidos</h1>

      {/* Botón Carrito */}
      <div className="mb-6">
        <button
          onClick={() => setShowCart(!showCart)}
          className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 relative"
        >
          🛒 Carrito
          {cart.length > 0 && (
            <span className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs">
              {cart.length}
            </span>
          )}
        </button>
      </div>

      {/* Carrito de Compras */}
      {showCart && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-2xl font-bold mb-4">Carrito de Compras</h2>
          
          {cart.length === 0 ? (
            <p className="text-gray-500">El carrito está vacío</p>
          ) : (
            <>
              <div className="space-y-4 mb-4">
                {cart.map(item => (
                  <div key={item.product_id} className="flex items-center justify-between border-b pb-4">
                    <div className="flex-1">
                      <h3 className="font-semibold">{item.product_name}</h3>
                      <p className="text-sm text-gray-600">${item.product_price} c/u</p>
                      <p className="text-sm text-gray-500">Stock: {item.stock}</p>
                    </div>
                    <div className="flex items-center space-x-3">
                      <button
                        onClick={() => updateCartQuantity(item.product_id, item.quantity - 1)}
                        className="bg-gray-200 px-2 py-1 rounded hover:bg-gray-300"
                      >
                        -
                      </button>
                      <span className="font-semibold">{item.quantity}</span>
                      <button
                        onClick={() => updateCartQuantity(item.product_id, item.quantity + 1)}
                        disabled={item.quantity >= item.stock}
                        className="bg-gray-200 px-2 py-1 rounded hover:bg-gray-300 disabled:opacity-50"
                      >
                        +
                      </button>
                      <span className="font-bold ml-4">${(item.product_price * item.quantity).toFixed(2)}</span>
                      <button
                        onClick={() => removeFromCart(item.product_id)}
                        className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 ml-2"
                      >
                        ✕
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              <div className="border-t pt-4">
                <div className="flex justify-between items-center mb-4">
                  <span className="text-xl font-bold">Total:</span>
                  <span className="text-2xl font-bold text-green-600">${calculateTotal()}</span>
                </div>

                <form onSubmit={createOrder}>
                  <textarea
                    placeholder="Notas del pedido (opcional)"
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    className="w-full border rounded p-2 mb-4"
                    rows="3"
                  />
                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-green-500 text-white py-3 rounded hover:bg-green-600 disabled:bg-gray-400"
                  >
                    {loading ? 'Procesando...' : `Confirmar Pedido - $${calculateTotal()}`}
                  </button>
                </form>
              </div>
            </>
          )}
        </div>
      )}

      {/* Lista de Productos */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-2xl font-bold mb-4">Productos Disponibles</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {products.map(product => (
            <div key={product.id} className="border rounded-lg p-4 hover:shadow-lg transition">
              {product.image && (
                <img
                  src={`http://localhost:8000${product.image}`}
                  alt={product.name}
                  className="w-full h-40 object-cover rounded mb-3"
                />
              )}
              <h3 className="font-bold text-lg mb-2">{product.name}</h3>
              <p className="text-gray-600 text-sm mb-2">{product.description}</p>
              <div className="flex justify-between items-center mb-3">
                <span className="text-2xl font-bold text-green-600">${product.price}</span>
                <span className={`text-sm ${product.stock > 0 ? 'text-gray-600' : 'text-red-600'}`}>
                  Stock: {product.stock}
                </span>
              </div>
              <button
                onClick={() => addToCart(product)}
                disabled={product.stock === 0}
                className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
              >
                {product.stock === 0 ? 'Sin Stock' : 'Agregar al Carrito'}
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Filtros */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-2xl font-bold mb-4">Mis Pedidos</h2>
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Filtrar por estado:</label>
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="border rounded p-2 w-full md:w-64"
          >
            <option value="">Todos</option>
            <option value="PENDING">Pendiente</option>
            <option value="PROCESSING">En Proceso</option>
            <option value="COMPLETED">Completado</option>
            <option value="CANCELLED">Cancelado</option>
          </select>
        </div>
      </div>

      {/* Historial de Pedidos */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold mb-4">Historial de Pedidos</h2>
        {orders.length === 0 ? (
          <p className="text-gray-500">No hay pedidos registrados</p>
        ) : (
          <div className="space-y-4">
            {orders.map(order => (
              <div key={order.id} className="border rounded-lg p-4 hover:shadow-lg transition">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h3 className="font-bold text-lg">Pedido #{order.id}</h3>
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
                    <p className="text-2xl font-bold text-green-600 mt-2">${order.total}</p>
                  </div>
                </div>

                {order.notes && (
                  <p className="text-sm text-gray-600 mb-3">
                    <span className="font-semibold">Notas:</span> {order.notes}
                  </p>
                )}

                <div className="border-t pt-3">
                  <h4 className="font-semibold mb-2">Items del pedido:</h4>
                  <div className="space-y-2">
                    {order.items.map(item => (
                      <div key={item.id} className="flex justify-between items-center text-sm">
                        <div className="flex items-center space-x-3">
                          {item.product_image && (
                            <img
                              src={`http://localhost:8000${item.product_image}`}
                              alt={item.product_name}
                              className="w-12 h-12 object-cover rounded"
                            />
                          )}
                          <div>
                            <span className="font-semibold">{item.product_name}</span>
                            <span className="text-gray-600"> x{item.quantity}</span>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-gray-600">${item.unit_price} c/u</p>
                          <p className="font-bold">${item.subtotal}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Orders;
