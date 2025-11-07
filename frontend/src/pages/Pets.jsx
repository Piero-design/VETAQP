import { useEffect, useState } from "react";
import { listPets, createPet } from "../api/catalogService";
import { useForm } from "react-hook-form";
import { TextField, Button } from "@mui/material";
import { toast } from "react-toastify";

export default function Pets() {
  const [pets, setPets] = useState([]);
  const { register, handleSubmit, reset } = useForm();

  async function load() {
    try { const { data } = await listPets(); setPets(data); }
    catch { setPets([]); }
  }
  useEffect(() => { load(); }, []);

  const onSubmit = async (d) => {
    await createPet({ name: d.name, species: d.species, age: Number(d.age) });
    toast.success("Mascota registrada");
    reset(); load();
  };

  return (
    <div className="grid md:grid-cols-2 gap-6">
      <div className="card p-6">
        <h2 className="text-lg font-semibold mb-3">Mis mascotas</h2>
        <ul className="space-y-2">
          {pets.map((p) => (
            <li key={p.id} className="flex justify-between border rounded-lg p-2">
              <span>{p.name} • {p.species} • {p.age} años</span>
            </li>
          ))}
          {pets.length === 0 && <p className="text-sm text-gray-500">No hay mascotas.</p>}
        </ul>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="card p-6 space-y-3">
        <h2 className="text-lg font-semibold">Agregar mascota</h2>
        <TextField label="Nombre" size="small" fullWidth {...register("name", { required: true })} />
        <TextField label="Especie" size="small" fullWidth {...register("species", { required: true })} />
        <TextField label="Edad" size="small" type="number" fullWidth {...register("age", { required: true, min: 0 })} />
        <Button type="submit" variant="contained">Guardar</Button>
      </form>
    </div>
  );
}
