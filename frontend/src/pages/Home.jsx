import { useEffect, useState } from "react";
import { listProducts } from "../api/catalogService";
import { useCart } from "../context/CartContext";  // ← para manejar el carrito

export default function Home() {
  const [items, setItems] = useState([]);
  const [q, setQ] = useState("");

  const { addToCart } = useCart(); // ← función global para agregar al carrito

  useEffect(() => {
    (async () => {
      try {
        const { data } = await listProducts();
        setItems(data);
      } catch {
        setItems([]);
      }
    })();
  }, []);

  const filtered = q
    ? items.filter((x) =>
        (x.name + x.description)
          .toLowerCase()
          .includes(q.toLowerCase())
      )
    : items;

  return (
    <div className="space-y-6">
      {/* Banner */}
      <div className="card p-6 bg-gradient-to-r from-brand/10 to-mint/10">
        <h1 className="text-2xl font-bold">Lo mejor para tu mascota</h1>
        <p className="text-gray-600">
          Productos y servicios seleccionados por veterinarios.
        </p>
        <div className="mt-4">
          <input
            className="input"
            placeholder="Buscar productos o servicios..."
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />
        </div>
      </div>

      {/* Productos */}
      <h2 className="text-lg font-semibold">Productos destacados</h2>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((p) => (
          <div key={p.id} className="card p-4">
            {/* Imagen desde URL */}
            <img
              className="w-full h-40 object-cover rounded-xl mb-3"
              src={p.image_url || "https://placehold.co/600x400"}
              alt={p.name}
            />

            {/* Información */}
            <h3 className="font-semibold">{p.name}</h3>
            <p className="text-sm text-gray-500">{p.description}</p>

            <div className="mt-3 flex items-center justify-between">
              <span className="font-semibold">
                S/ {Number(p.price).toFixed(2)}
              </span>

              {/* Botón agregar al carrito */}
              <button
                className="btn-primary"
                onClick={() => addToCart(p)}
              >
                Agregar
              </button>
            </div>
          </div>
        ))}

        {filtered.length === 0 && (
          <div className="text-sm text-gray-500">No hay productos (aún).</div>
        )}
      </div>

      {/* Servicios */}
      <h2 className="text-lg font-semibold">Servicios más solicitados</h2>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {["Consulta médica", "Baño y corte", "Vacunación"].map((s, i) => (
          <div key={i} className="card p-5">
            <h3 className="font-semibold">{s}</h3>
            <p className="text-sm text-gray-500">
              Agenda tu cita con nuestros especialistas.
            </p>
            <button className="btn-primary mt-3">Reservar</button>
          </div>
        ))}
      </div>
    </div>
  );
}
