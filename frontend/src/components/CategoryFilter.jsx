import { useEffect, useState } from 'react';
import { getCategories, getPetTypes } from '../api/categoryService';
import { Link } from 'react-router-dom';

export function CategoryFilter({ onCategoryChange, onPetTypeChange }) {
  const [categories, setCategories] = useState([]);
  const [petTypes, setPetTypes] = useState([]);
  const [selectedPetType, setSelectedPetType] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [catRes, petRes] = await Promise.all([
          getCategories(),
          getPetTypes()
        ]);
        setCategories(catRes.data);
        setPetTypes(petRes.data);
      } catch (error) {
        console.error('Error cargando categorías:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const filteredCategories = selectedPetType
    ? categories.filter(cat => cat.pet_type?.id === parseInt(selectedPetType))
    : categories;

  const handlePetTypeChange = (e) => {
    const value = e.target.value;
    setSelectedPetType(value);
    onPetTypeChange?.(value);
  };

  if (loading) {
    return <div className="card p-4 text-center">Cargando categorías...</div>;
  }

  return (
    <div className="card p-4 space-y-4">
      <h3 className="font-bold text-lg">Categorías</h3>

      {/* Filtro por tipo de mascota */}
      <div>
        <label className="block text-sm font-semibold mb-2">Tipo de Mascota</label>
        <select
          value={selectedPetType}
          onChange={handlePetTypeChange}
          className="input w-full"
        >
          <option value="">Todas las mascotas</option>
          {petTypes.map(pet => (
            <option key={pet.id} value={pet.id}>
              {pet.name === 'dog' ? '🐕 Perros' : '🐱 Gatos'}
            </option>
          ))}
        </select>
      </div>

      {/* Categorías */}
      <div className="space-y-2">
        {filteredCategories.length > 0 ? (
          filteredCategories.map(category => (
            <Link
              key={category.id}
              to={`/catalogo?category=${category.id}`}
              className="block p-2 hover:bg-brand hover:text-white transition rounded-md text-sm"
              onClick={() => onCategoryChange?.(category.id)}
            >
              {category.icon && <span className="mr-2">{category.icon}</span>}
              {category.name}
            </Link>
          ))
        ) : (
          <p className="text-sm text-gray-500">No hay categorías disponibles</p>
        )}
      </div>
    </div>
  );
}
