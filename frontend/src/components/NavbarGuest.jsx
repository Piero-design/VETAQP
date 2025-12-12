import { Link } from "react-router-dom";

export function NavbarGuest() {
  return (
    <div className="flex items-center gap-2 animate-fadeIn">
      <Link 
        to="/login" 
        className="px-4 py-2 text-gray-700 hover:text-brand transition-colors duration-200"
      >
        Ingresar
      </Link>
      <Link 
        to="/register" 
        className="px-4 py-2 bg-brand text-white rounded-lg hover:bg-brand/90 transition-colors duration-200"
      >
        Crear cuenta
      </Link>
    </div>
  );
}
