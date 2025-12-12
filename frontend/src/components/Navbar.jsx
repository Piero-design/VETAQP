// src/components/Navbar.jsx

import { Link, useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import { getProfile } from "../api/userService";
import PetsIcon from "@mui/icons-material/Pets";
import ShoppingCartCheckoutIcon from "@mui/icons-material/ShoppingCartCheckout";

export default function Navbar() {
  const [user, setUser] = useState(null);
  const nav = useNavigate();
  const loc = useLocation();

  // CADA VEZ QUE CAMBIA LA RUTA, SE VERIFICA EL USUARIO
  useEffect(() => {
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
    nav("/");
  };

  const link = "hover:text-brand transition whitespace-nowrap";

  return (
    <header className="bg-white/90 backdrop-blur border-b shadow-sm">
      <div className="max-w-7xl mx-auto h-16 px-6 flex items-center justify-between">

        {/* LOGO */}
        <Link to="/" className="flex items-center gap-2 text-2xl font-bold text-brand mr-6">
          <PetsIcon /> AqpVet
        </Link>

        {/* MENÚ */}
        <nav className="hidden xl:flex items-center gap-8 text-sm font-medium text-gray-700">
          <Link className={link} to="/">Inicio</Link>
          <Link className={link} to="/catalogo">Catálogo</Link>
          <Link className={link} to="/appointments">Citas</Link>
          <Link className={link} to="/chat">Chat</Link>

          <div className="w-px h-5 bg-gray-300"></div>
          <Link className={link} to="/pets">Mascotas</Link>
          <Link className={link} to="/medical-history">Historial Médico</Link>

          <div className="w-px h-5 bg-gray-300"></div>
          <Link className={link} to="/inventory">Inventario</Link>
          <Link className={link} to="/payments">Pagos</Link>
          <Link className={link} to="/memberships">Membresías</Link>

          <div className="w-px h-5 bg-gray-300"></div>
          <Link className={link} to="/orders">Pedidos</Link>
          <Link className={link} to="/order-tracking">Seguimiento</Link>
          <Link className={link} to="/notifications">Notificaciones</Link>

          {user?.is_staff && (
            <Link className={`${link} text-blue-600 font-semibold`} to="/dashboard">
              📊 Dashboard
            </Link>
          )}
        </nav>

        {/* DERECHA */}
        <div className="flex items-center gap-4">

          {/* CARRITO */}
          <Link to="/cart" className="btn-ghost !px-3">
            <ShoppingCartCheckoutIcon fontSize="small" />
          </Link>

          {/* NO LOGUEADO */}
          {!user && (
            <>
              <Link to="/login" className="btn-ghost">Ingresar</Link>
              <Link to="/register" className="btn-primary">Crear cuenta</Link>
            </>
          )}

          {/* LOGUEADO */}
          {user && (
            <div className="flex items-center gap-3 whitespace-nowrap">
              <span className="font-semibold text-gray-700">
                Hola, {user.username}
              </span>
              <button onClick={logout} className="btn-primary">Salir</button>
            </div>
          )}

        </div>

      </div>
    </header>
  );
}
