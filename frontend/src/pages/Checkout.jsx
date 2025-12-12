import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useCart } from "../context/CartContext";
import { createOrder, confirmPayment } from "../api/orderService";
import { getProfile } from "../api/userService";
import { toast } from "react-toastify";

export default function Checkout() {
  const navigate = useNavigate();
  const { cart, totalPrice, clearCart } = useCart();
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState("shipping");
  const [user, setUser] = useState(null);
  const [authChecking, setAuthChecking] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (!token) {
      toast.error("Debes iniciar sesión para continuar");
      navigate("/login");
      return;
    }

    (async () => {
      try {
        const { data } = await getProfile();
        setUser(data);
      } catch {
        toast.error("Sesión expirada. Por favor, inicia sesión de nuevo");
        localStorage.clear();
        navigate("/login");
      } finally {
        setAuthChecking(false);
      }
    })();
  }, [navigate]);
  const [formData, setFormData] = useState({
    shipping_name: "",
    shipping_email: "",
    shipping_phone: "",
    shipping_address: "",
    shipping_city: "",
  });

  if (authChecking) {
    return (
      <div className="card p-6 text-center">
        <p className="text-gray-500">Verificando autenticación...</p>
      </div>
    );
  }

  if (cart.length === 0) {
    return (
      <div className="card p-6 text-center">
        <p className="text-gray-500 mb-4">Tu carrito está vacío</p>
        <button onClick={() => navigate("/")} className="btn-primary">
          Volver al catálogo
        </button>
      </div>
    );
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmitShipping = (e) => {
    e.preventDefault();
    if (Object.values(formData).some((v) => !v)) {
      toast.error("Completa todos los campos");
      return;
    }
    setStep("payment");
  };

  const handlePayment = async () => {
    setLoading(true);
    try {
      const items = cart.map((item) => ({
        product_id: item.id,
        quantity: item.quantity,
      }));

      const response = await createOrder({
        ...formData,
        items,
      });

      const orderId = response.data.id;
      await confirmPayment(orderId);

      clearCart();
      toast.success("¡Pedido confirmado!");
      navigate(`/order-confirmation/${orderId}`);
    } catch (error) {
      toast.error(error.response?.data?.error || "Error al procesar el pedido");
    } finally {
      setLoading(false);
    }
  };

  const tax = totalPrice * 0.18;
  const shipping = 0;
  const total = totalPrice + tax + shipping;

  return (
    <div className="grid lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2">
        {step === "shipping" && (
          <form onSubmit={handleSubmitShipping} className="card p-6 space-y-4">
            <h2 className="text-2xl font-bold">Datos de envío</h2>

            <div>
              <label className="block text-sm font-semibold mb-1">Nombre completo</label>
              <input
                type="text"
                name="shipping_name"
                value={formData.shipping_name}
                onChange={handleInputChange}
                className="input"
                placeholder="Juan Pérez"
              />
            </div>

            <div className="grid sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-semibold mb-1">Email</label>
                <input
                  type="email"
                  name="shipping_email"
                  value={formData.shipping_email}
                  onChange={handleInputChange}
                  className="input"
                  placeholder="juan@example.com"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold mb-1">Teléfono</label>
                <input
                  type="tel"
                  name="shipping_phone"
                  value={formData.shipping_phone}
                  onChange={handleInputChange}
                  className="input"
                  placeholder="+51 999 999 999"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold mb-1">Dirección</label>
              <textarea
                name="shipping_address"
                value={formData.shipping_address}
                onChange={handleInputChange}
                className="input"
                rows="3"
                placeholder="Calle, número, apartamento..."
              />
            </div>

            <div>
              <label className="block text-sm font-semibold mb-1">Ciudad/Región</label>
              <input
                type="text"
                name="shipping_city"
                value={formData.shipping_city}
                onChange={handleInputChange}
                className="input"
                placeholder="Arequipa"
              />
            </div>

            <button type="submit" className="btn-primary w-full">
              Continuar al pago
            </button>
          </form>
        )}

        {step === "payment" && (
          <div className="card p-6 space-y-4">
            <h2 className="text-2xl font-bold">Pago</h2>

            <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
              <p className="text-sm text-gray-600 mb-3">
                <strong>Nota:</strong> Este es un pago simulado para demostración.
              </p>
              <div className="space-y-2 text-sm">
                <p><strong>Número de tarjeta:</strong> 4532 1234 5678 9010</p>
                <p><strong>Vencimiento:</strong> 12/25</p>
                <p><strong>CVV:</strong> 123</p>
              </div>
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => setStep("shipping")}
                className="btn-secondary flex-1"
              >
                Atrás
              </button>
              <button
                onClick={handlePayment}
                disabled={loading}
                className="btn-primary flex-1"
              >
                {loading ? "Procesando..." : "Confirmar pago"}
              </button>
            </div>
          </div>
        )}
      </div>

      <div className="card p-6 h-fit sticky top-6">
        <h3 className="text-lg font-bold mb-4">Resumen</h3>

        <div className="space-y-2 mb-4 max-h-64 overflow-y-auto">
          {cart.map((item) => {
            const price = item.final_price ? Number(item.final_price) : Number(item.price);
            return (
              <div key={item.id} className="flex justify-between text-sm">
                <span>{item.name} x{item.quantity}</span>
                <span>S/ {(price * item.quantity).toFixed(2)}</span>
              </div>
            );
          })}
        </div>

        <div className="border-t pt-3 space-y-2 text-sm">
          <div className="flex justify-between">
            <span>Subtotal:</span>
            <span>S/ {totalPrice.toFixed(2)}</span>
          </div>
          <div className="flex justify-between">
            <span>Impuesto (18%):</span>
            <span>S/ {tax.toFixed(2)}</span>
          </div>
          <div className="flex justify-between">
            <span>Envío:</span>
            <span>S/ {shipping.toFixed(2)}</span>
          </div>
          <div className="flex justify-between text-lg font-bold border-t pt-2">
            <span>Total:</span>
            <span>S/ {total.toFixed(2)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
