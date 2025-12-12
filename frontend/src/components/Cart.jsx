import { useCart } from "../context/CartContext";
import { Link } from "react-router-dom";

export default function Cart() {
  const { cart, removeFromCart, decreaseItem, totalPrice, totalItems } = useCart();

  if (cart.length === 0) {
    return (
      <div className="card p-6 text-center">
        <p className="text-gray-500 mb-4">Tu carrito está vacío</p>
        <Link to="/" className="btn-primary">
          Continuar comprando
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">Carrito ({totalItems} items)</h2>
      
      <div className="card p-4 space-y-3">
        {cart.map((item) => {
          const price = item.final_price ? Number(item.final_price) : Number(item.price);
          const subtotal = price * item.quantity;
          
          return (
            <div key={item.id} className="flex items-center justify-between border-b pb-3">
              <div className="flex-1">
                <h3 className="font-semibold">{item.name}</h3>
                <p className="text-sm text-gray-500">S/ {price.toFixed(2)} x {item.quantity}</p>
              </div>
              
              <div className="flex items-center gap-2">
                <span className="font-semibold">S/ {subtotal.toFixed(2)}</span>
                
                <div className="flex gap-1">
                  <button
                    onClick={() => decreaseItem(item.id)}
                    className="btn-sm bg-gray-200 hover:bg-gray-300"
                  >
                    -
                  </button>
                  <button
                    onClick={() => removeFromCart(item.id)}
                    className="btn-sm bg-red-200 hover:bg-red-300 text-red-700"
                  >
                    ✕
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="card p-4 bg-gray-50">
        <div className="flex justify-between text-lg font-bold mb-4">
          <span>Total:</span>
          <span>S/ {totalPrice.toFixed(2)}</span>
        </div>
        
        <Link to="/checkout" className="btn-primary w-full text-center">
          Ir al Checkout
        </Link>
      </div>
    </div>
  );
}
