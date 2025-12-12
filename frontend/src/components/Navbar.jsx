import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useCart } from "../context/CartContext";
import { NavDropdown } from "./NavDropdown";
import { NavbarGuest } from "./NavbarGuest";
import { NavbarUser } from "./NavbarUser";
import { useMemo } from "react";

import PetsIcon from "@mui/icons-material/Pets";
import ShoppingCartCheckoutIcon from "@mui/icons-material/ShoppingCartCheckout";

export default function Navbar() {
  const { user, loading, logout, displayName, isStaff } = useAuth();
  const { totalItems } = useCart();

  // Memoizar arrays para evitar re-renders innecesarios
  const serviciosItems = useMemo(
    () => [
      { label: 'Citas Veterinarias', href: '/appointments' },
      { label: 'Chat con Veterinario', href: '/chat' },
      { label: 'Historial Médico', href: '/medical-history' },
      { label: 'Seguimiento de Pedidos', href: '/order-tracking' },
    ],
    []
  );

  const tiendaItems = useMemo(
    () => [
      { label: 'Catálogo Completo', href: '/catalogo' },
      { label: 'Alimentos', href: '/catalogo?category=alimentos' },
      { label: 'Accesorios', href: '/catalogo?category=accesorios' },
      { label: 'Higiene', href: '/catalogo?category=higiene' },
      { label: 'Medicamentos', href: '/catalogo?category=medicamentos' },
      { label: 'Juguetes', href: '/catalogo?category=juguetes' },
      { divider: true },
      { label: 'Mis Pedidos', href: '/orders' },
      { label: 'Membresías', href: '/memberships' },
    ],
    []
  );

  const adminItems = useMemo(
    () => [
      { label: 'Inventario', href: '/inventory' },
      { label: 'Dashboard', href: '/dashboard' },
      { label: 'Notificaciones', href: '/notifications' },
    ],
    []
  );

  // Mantener altura consistente durante loading
  return (
    <header className="bg-white shadow border-b sticky top-0 z-50">
      <div className="max-w-7xl mx-auto h-16 px-4 flex items-center justify-between">

        {/* LOGO */}
        <Link to="/" className="flex items-center gap-2 text-xl font-bold text-brand hover:opacity-80 transition-opacity duration-200">
          <PetsIcon /> AqpVet
        </Link>

        {/* MENÚ PRINCIPAL */}
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium">
          <Link 
            className="text-gray-700 hover:text-brand transition-colors duration-200" 
            to="/"
          >
            Inicio
          </Link>
          <NavDropdown label="Servicios" items={serviciosItems} />
          <NavDropdown label="Tienda" items={tiendaItems} />
          {isStaff && (
            <NavDropdown 
              label="Admin" 
              items={adminItems} 
              color="text-blue-600"
            />
          )}
        </nav>

        {/* DERECHA: CARRITO + USUARIO */}
        <div className="flex items-center gap-4">

          {/* CARRITO */}
          <Link 
            to="/cart" 
            className="relative text-gray-700 hover:text-brand transition-colors duration-200 p-2"
          >
            <ShoppingCartCheckoutIcon fontSize="small" />
            {totalItems > 0 && (
              <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs w-5 h-5 flex items-center justify-center rounded-full font-bold animate-pulse">
                {totalItems}
              </span>
            )}
          </Link>

          {/* AUTENTICACIÓN - Componentes separados */}
          <div className="min-w-[200px]">
            {loading ? (
              <div className="h-10 bg-gray-200 rounded animate-pulse" />
            ) : user ? (
              <NavbarUser displayName={displayName} logout={logout} />
            ) : (
              <NavbarGuest />
            )}
          </div>

        </div>
      </div>
    </header>
  );
}
