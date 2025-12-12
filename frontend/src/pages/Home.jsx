import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { listProducts } from "../api/catalogService";
import { useCart } from "../context/CartContext";
import { CategoryFilter } from "../components/CategoryFilter";
import { toast } from "react-toastify";

export default function Home() {
  const [items, setItems] = useState([]);
  const [q, setQ] = useState("");
  const [petType, setPetType] = useState("");
  const [category, setCategory] = useState("");
  const [loading, setLoading] = useState(true);
  const [searchParams] = useSearchParams();
  const { addToCart } = useCart();

  useEffect(() => {
    const categoryFromUrl = searchParams.get('category');
    if (categoryFromUrl) {
      setCategory(categoryFromUrl);
    }
  }, [searchParams]);

  useEffect(() => {
    (async () => {
      setLoading(true);
      try {
        const { data } = await listProducts();
        setItems(data);
      } catch (error) {
        toast.error("Error al cargar productos");
        setItems([]);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const filtered = items.filter((x) => {
    const matchesQuery = !q || (x.name + x.description).toLowerCase().includes(q.toLowerCase());
    const matchesPet = !petType || x.pet_type?.id === parseInt(petType);
    const matchesCategory = !category || x.category?.id === parseInt(category);
    return matchesQuery && matchesPet && matchesCategory;
  });

  const featured = filtered.filter((p) => p.discount_price).slice(0, 6);
  const newest = filtered.slice(0, 6);

  const handleAddToCart = (product) => {
    if (!product.stock || product.stock <= 0) {
      toast.error("Producto sin stock");
      return;
    }
    addToCart(product);
    toast.success(`${product.name} agregado al carrito`);
  };

  const ProductCard = ({ p }) => {
    const hasDiscount = p.discount_price && p.discount_price < p.price;
    const discountPercent = hasDiscount ? Math.round(((p.price - p.discount_price) / p.price) * 100) : 0;

    return (
      <div className="card p-4 hover:shadow-lg transition">
        <div className="relative mb-3">
          <img
            className="w-full h-40 object-cover rounded-lg"
            src={p.image_url || p.image || "https://placehold.co/600x400"}
            alt={p.name}
          />
          {hasDiscount && (
            <div className="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 rounded text-xs font-bold">
              -{discountPercent}%
            </div>
          )}
          {p.is_low_stock && (
            <div className="absolute top-2 left-2 bg-yellow-500 text-white px-2 py-1 rounded text-xs font-bold">
              Stock bajo
            </div>
          )}
        </div>

        <h3 className="font-semibold text-sm line-clamp-2">{p.name}</h3>
        {p.brand && <p className="text-xs text-gray-500">{p.brand}</p>}
        <p className="text-xs text-gray-500 line-clamp-1 mt-1">{p.description}</p>

        <div className="mt-3 flex items-center justify-between">
          <div className="flex flex-col">
            {hasDiscount ? (
              <>
                <span className="text-xs line-through text-gray-400">
                  S/ {Number(p.price).toFixed(2)}
                </span>
                <span className="font-bold text-green-600">
                  S/ {Number(p.final_price).toFixed(2)}
                </span>
              </>
            ) : (
              <span className="font-semibold">
                S/ {Number(p.price).toFixed(2)}
              </span>
            )}
          </div>

          <button
            className="btn-primary text-sm"
            onClick={() => handleAddToCart(p)}
            disabled={!p.stock || p.stock <= 0}
          >
            {p.stock && p.stock > 0 ? "Agregar" : "Sin stock"}
          </button>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-8">
      {/* Hero Banner */}
      <div className="card p-8 bg-gradient-to-r from-brand/20 to-mint/20 rounded-2xl">
        <div className="max-w-2xl">
          <h1 className="text-4xl font-bold mb-2">Lo mejor para tu mascota</h1>
          <p className="text-gray-600 mb-6">
            Productos y servicios seleccionados por veterinarios. Envío rápido a todo Arequipa.
          </p>
        </div>
      </div>

      {/* Layout con Sidebar de Categorías */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {/* SIDEBAR - Categorías (solo en desktop) */}
        <aside className="hidden md:block">
          <CategoryFilter 
            onCategoryChange={setCategory}
            onPetTypeChange={setPetType}
          />
        </aside>

        {/* CONTENIDO PRINCIPAL */}
        <main className="md:col-span-3 space-y-6">
          {/* Búsqueda */}
          <div className="card p-4">
            <input
              type="text"
              placeholder="Buscar productos..."
              value={q}
              onChange={(e) => setQ(e.target.value)}
              className="input w-full"
            />
          </div>

          {loading ? (
            <div className="text-center py-12">Cargando productos...</div>
          ) : (
            <>
              {/* Productos con descuento */}
              {featured.length > 0 && (
                <section>
                  <h2 className="text-2xl font-bold mb-4">🔥 Ofertas especiales</h2>
                  <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {featured.map((p) => (
                      <ProductCard key={p.id} p={p} />
                    ))}
                  </div>
                </section>
              )}

              {/* Productos destacados */}
              <section>
                <h2 className="text-2xl font-bold mb-4">✨ Productos destacados</h2>
                <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  {filtered.length > 0 ? (
                    filtered.map((p) => (
                      <ProductCard key={p.id} p={p} />
                    ))
                  ) : (
                    <div className="col-span-full text-center py-8 text-gray-500">
                      No hay productos disponibles
                    </div>
                  )}
                </div>
              </section>

              {/* Beneficios */}
              <section className="grid sm:grid-cols-3 gap-4">
                {[
                  { icon: "🚚", title: "Envío rápido", desc: "A domicilio en 24-48h" },
                  { icon: "✅", title: "Garantizado", desc: "Productos de calidad" },
                  { icon: "💬", title: "Soporte", desc: "Atención al cliente 24/7" },
                ].map((b, i) => (
                  <div key={i} className="card p-6 text-center">
                    <div className="text-4xl mb-2">{b.icon}</div>
                    <h3 className="font-bold">{b.title}</h3>
                    <p className="text-sm text-gray-500">{b.desc}</p>
                  </div>
                ))}
              </section>
            </>
          )}
        </main>
      </div>
    </div>
  );
}
