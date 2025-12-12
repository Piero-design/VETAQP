import { Link, useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import { getProfile } from "../api/userService";
import { useCart } from "../context/CartContext";

import PetsIcon from "@mui/icons-material/Pets";
import ShoppingCartCheckoutIcon from "@mui/icons-material/ShoppingCartCheckout";

export default function Navbar() {
  const [user, setUser] = useState(null);
  const nav = useNavigate();
  const loc = useLocation();
  const { totalItems } = useCart();

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (!token) {
      setUser(null);
      return;
    }

    (async () => {
      try {
        const { data } = await getProfile();
        setUser(data);
      } catch {
        setUser(null);
      }
    })();
  }, [loc.pathname]);

  const logout = () => {
    localStorage.clear();
    setUser(null);
    nav("/login");
  };

  const link = "block px-2 py-1 hover:text-brand transition";

  return (
    <header className="bg-white shadow border-b sticky top-0 z-50">
      <div className="max-w-7xl mx-auto h-16 px-4 flex items-center justify-between">

        {/* LOGO */}
        <Link to="/" className="flex items-center gap-2 text-xl font-bold text-brand">
          <PetsIcon /> AqpVet
        </Link>

        {/* MEGA MENÚ */}
        <nav className="hidden md:flex items-center gap-10 text-sm font-medium">

          {/* INICIO */}
          <Link className="hover:text-brand transition" to="/">Inicio</Link>

          {/* SERVICIOS */}
          <div className="relative group">
            <span className="cursor-pointer hover:text-brand">Servicios ▾</span>

            <div className="absolute left-0 hidden group-hover:flex bg-white shadow-lg rounded-md mt-3 p-4 w-64 flex-col z-50">
              <Link className={link} to="/appointments">Citas</Link>
              <Link className={link} to="/chat">Chat</Link>
              <Link className={link} to="/medical-history">Historial Médico</Link>
              <Link className={link} to="/order-tracking">Seguimiento</Link>
            </div>
          </div>

          {/* TIENDA */}
          <div className="relative group">
            <span className="cursor-pointer hover:text-brand">Tienda ▾</span>

            <div className="absolute left-0 hidden group-hover:flex bg-white shadow-lg rounded-md mt-3 p-4 w-64 flex-col z-50">
              <Link className={link} to="/catalogo">Catálogo</Link>
              <Link className={link} to="/orders">Pedidos</Link>
              <Link className={link} to="/memberships">Membresías</Link>
              <Link className={link} to="/payments">Pagos</Link>
            </div>
          </div>

          {/* ADMINISTRACIÓN (solo STAFF) */}
          {user?.is_staff && (
            <div className="relative group">
              <span className="cursor-pointer hover:text-brand text-blue-600">
                Administración ▾
              </span>

              <div className="absolute left-0 hidden group-hover:flex bg-white shadow-lg rounded-md mt-3 p-4 w-64 flex-col z-50">
                <Link className={link} to="/inventory">Inventario</Link>
                <Link className={link} to="/dashboard">Dashboard</Link>
                <Link className={link} to="/notifications">Notificaciones</Link>
              </div>
            </div>
          )}

        </nav>

        {/* DERECHA: CARRITO + USUARIO */}
        <div className="flex items-center gap-4">

          {/* CARRITO */}
          <Link to="/cart" className="relative btn-ghost !px-3">
            <ShoppingCartCheckoutIcon fontSize="small" />
            {totalItems > 0 && (
              <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs w-5 h-5 flex items-center justify-center rounded-full">
                {totalItems}
              </span>
            )}
          </Link>

          {/* USUARIO */}
          {user ? (
            <>
              <Link to="/profile" className="btn-ghost">{user.username}</Link>
              <button onClick={logout} className="btn-primary">Salir</button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn-ghost">Ingresar</Link>
              <Link to="/register" className="btn-primary">Crear cuenta</Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
