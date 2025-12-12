import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getOrder } from "../api/orderService";
import { toast } from "react-toastify";

export default function OrderConfirmation() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const response = await getOrder(id);
        setOrder(response.data);
      } catch (error) {
        toast.error("No se pudo cargar el pedido");
        navigate("/");
      } finally {
        setLoading(false);
      }
    })();
  }, [id, navigate]);

  if (loading) {
    return <div className="text-center py-8">Cargando...</div>;
  }

  if (!order) {
    return <div className="text-center py-8">Pedido no encontrado</div>;
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="card p-6 text-center bg-green-50 border-2 border-green-200">
        <h1 className="text-3xl font-bold text-green-700 mb-2">¡Pedido Confirmado!</h1>
        <p className="text-gray-600">Tu pedido ha sido procesado exitosamente</p>
      </div>

      <div className="card p-6">
        <h2 className="text-xl font-bold mb-4">Detalles del Pedido</h2>

        <div className="grid sm:grid-cols-2 gap-4 mb-6">
          <div>
            <p className="text-sm text-gray-500">Número de pedido</p>
            <p className="font-semibold text-lg">{order.order_number}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Estado</p>
            <p className="font-semibold text-lg capitalize">{order.status}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Fecha</p>
            <p className="font-semibold">{new Date(order.created_at).toLocaleDateString()}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Total</p>
            <p className="font-semibold text-lg">S/ {Number(order.total).toFixed(2)}</p>
          </div>
        </div>

        <h3 className="font-bold mb-3">Datos de envío</h3>
        <div className="bg-gray-50 p-4 rounded-lg text-sm space-y-1 mb-6">
          <p><strong>{order.shipping_name}</strong></p>
          <p>{order.shipping_address}</p>
          <p>{order.shipping_city}</p>
          <p>{order.shipping_email}</p>
          <p>{order.shipping_phone}</p>
        </div>

        <h3 className="font-bold mb-3">Productos</h3>
        <div className="space-y-2 mb-6">
          {order.items.map((item) => (
            <div key={item.id} className="flex justify-between text-sm border-b pb-2">
              <span>{item.product.name}</span>
              <span>x{item.quantity} - S/ {(Number(item.price) * item.quantity).toFixed(2)}</span>
            </div>
          ))}
        </div>

        <div className="bg-gray-50 p-4 rounded-lg space-y-2 text-sm mb-6">
          <div className="flex justify-between">
            <span>Subtotal:</span>
            <span>S/ {Number(order.subtotal).toFixed(2)}</span>
          </div>
          <div className="flex justify-between">
            <span>Impuesto:</span>
            <span>S/ {Number(order.tax).toFixed(2)}</span>
          </div>
          <div className="flex justify-between">
            <span>Envío:</span>
            <span>S/ {Number(order.shipping_cost).toFixed(2)}</span>
          </div>
          <div className="flex justify-between font-bold text-base border-t pt-2">
            <span>Total:</span>
            <span>S/ {Number(order.total).toFixed(2)}</span>
          </div>
        </div>

        <div className="flex gap-3">
          <button onClick={() => navigate("/orders")} className="btn-secondary flex-1">
            Ver mis pedidos
          </button>
          <button onClick={() => navigate("/")} className="btn-primary flex-1">
            Continuar comprando
          </button>
        </div>
      </div>
    </div>
  );
}
