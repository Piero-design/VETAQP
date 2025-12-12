import { useCart } from "../context/CartContext";
import { useNavigate } from "react-router-dom";

export default function Cart() {
  const navigate = useNavigate();
  const {
    cart,
    addToCart,
    decreaseItem,
    removeFromCart,
    clearCart,
    totalItems,
    totalPrice,
  } = useCart();

  return (
    <div className="max-w-3xl mx-auto space-y-6 p-4">
      <h1 className="text-2xl font-bold">🛒 Carrito de compras</h1>

      {cart.length === 0 ? (
        <div className="card p-6 text-center text-gray-500">
          Tu carrito está vacío.
        </div>
      ) : (
        <>
          <div className="space-y-4">
            {cart.map((item) => (
              <div key={item.id} className="card p-4 flex items-center gap-4">
                <img
                  src={item.image_url || item.image || "https://placehold.co/150"}
                  className="w-24 h-24 object-cover rounded-lg"
                />

                <div className="flex-1">
                  <h2 className="font-semibold">{item.name}</h2>
                  <p className="text-gray-500 text-sm">{item.description}</p>

                  <div className="flex items-center gap-3 mt-2">
                    <button
                      className="btn-ghost !px-3"
                      onClick={() => decreaseItem(item.id)}
                    >
                      −
                    </button>

                    <span className="font-bold w-6 text-center">{item.quantity}</span>

                    <button
                      className="btn-ghost !px-3"
                      onClick={() => addToCart(item)}
                    >
                      +
                    </button>
                  </div>
                </div>

                <div className="text-right">
                  <p className="font-semibold">
                    S/ {(item.price * item.quantity).toFixed(2)}
                  </p>

                  <button
                    className="text-red-500 text-sm hover:underline mt-1"
                    onClick={() => removeFromCart(item.id)}
                  >
                    Eliminar
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Totales */}
          <div className="card p-4">
            <p className="text-lg font-semibold">
              Total items: <span className="text-brand">{totalItems}</span>
            </p>
            <p className="text-xl font-bold">
              Total a pagar: S/ {totalPrice.toFixed(2)}
            </p>

            <button 
              className="btn-primary w-full mt-3"
              onClick={() => navigate("/checkout")}
            >
              Proceder al pago
            </button>

            <button
              className="btn-ghost w-full mt-2 text-red-500"
              onClick={clearCart}
            >
              Vaciar carrito
            </button>
          </div>
        </>
      )}
    </div>
  );
}
