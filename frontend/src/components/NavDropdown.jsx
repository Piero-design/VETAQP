import { useState, useRef, useEffect } from "react";
import { Link } from "react-router-dom";

export function NavDropdown({ label, items, color = "text-gray-800" }) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);
  const timeoutRef = useRef(null);

  // Cerrar dropdown cuando se hace click fuera
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }

    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
      return () => document.removeEventListener("mousedown", handleClickOutside);
    }
  }, [isOpen]);

  // Manejar mouse enter con delay
  const handleMouseEnter = () => {
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    setIsOpen(true);
  };

  // Manejar mouse leave con delay
  const handleMouseLeave = () => {
    timeoutRef.current = setTimeout(() => {
      setIsOpen(false);
    }, 150);
  };

  return (
    <div
      ref={dropdownRef}
      className="relative"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      {/* BOTÓN */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`flex items-center gap-1 ${color} hover:text-brand transition-colors duration-200 cursor-pointer font-medium`}
      >
        {label}
        <span
          className={`transition-transform duration-200 ${
            isOpen ? "rotate-180" : ""
          }`}
        >
          ▾
        </span>
      </button>

      {/* DROPDOWN */}
      {isOpen && (
        <div
          className="
            absolute left-0 top-full mt-2
            bg-white shadow-lg rounded-lg
            p-2 w-56
            z-50
            animate-fadeIn
            border border-gray-100
          "
        >
          {items.map((item, idx) => (
            <div key={idx}>
              {item.divider ? (
                <hr className="my-2" />
              ) : (
                <Link
                  to={item.href}
                  className="
                    block px-3 py-2
                    hover:bg-gray-100 hover:text-brand
                    transition-colors duration-150 rounded-md text-sm
                    text-gray-700
                  "
                >
                  {item.label}
                </Link>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
