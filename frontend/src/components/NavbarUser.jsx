import { Link } from "react-router-dom";

export function NavbarUser({ displayName, logout }) {
  return (
    <div className="flex items-center gap-3 animate-fadeIn">
      <div className="text-right">
        <p className="text-sm font-semibold text-gray-800">👋 Hola, {displayName}</p>
        <Link 
          to="/profile" 
          className="text-xs text-gray-500 hover:text-brand transition-colors duration-200"
        >
          Ver perfil
        </Link>
      </div>
      <button
        onClick={logout}
        className="px-4 py-2 bg-brand text-white rounded-lg hover:bg-brand/90 transition-colors duration-200"
      >
        Salir
      </button>
    </div>
  );
}
