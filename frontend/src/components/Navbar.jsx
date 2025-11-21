import { Link, useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import { getProfile } from "../api/userService";
import PetsIcon from "@mui/icons-material/Pets";
import ShoppingCartCheckoutIcon from "@mui/icons-material/ShoppingCartCheckout";

export default function Navbar() {
  const [user, setUser] = useState(null);
  const nav = useNavigate();
  const loc = useLocation();

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

  const link = "hover:text-brand transition";
  return (
    <header className="bg-white/90 backdrop-blur border-b">
      <div className="max-w-7xl mx-auto h-16 px-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 text-xl font-bold text-brand">
          <PetsIcon /> AqpVet
        </Link>
        <nav className="hidden md:flex items-center gap-6 text-sm">
          <Link className={link} to="/">Inicio</Link>
          <Link className={link} to="/catalogo">Catálogo</Link>
          <Link className={link} to="/citas">Citas</Link>
          <Link className={link} to="/promos">Promos</Link>
          <Link className={link} to="/pets">Mascotas</Link>
          <Link className={link} to="/inventory">Inventario</Link>
          <Link className={link} to="/payments">Pagos</Link>
          <Link className={link} to="/memberships">Membresías</Link>
        </nav>
        <div className="flex items-center gap-3">
          <Link to="/cart" className="btn-ghost !px-3">
            <ShoppingCartCheckoutIcon fontSize="small" />
          </Link>
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
