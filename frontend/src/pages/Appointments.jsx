import { useEffect, useMemo, useState } from "react";
import { useForm } from "react-hook-form";
import { TextField, Button, MenuItem } from "@mui/material";
import { toast } from "react-toastify";

import { listAppointments, createAppointment, updateAppointment } from "../api/appointmentsService";
import { listPets } from "../api/catalogService";

const STATUS_LABEL = {
  scheduled: "Programada",
  completed: "Completada",
  cancelled: "Cancelada",
};

const statusTone = {
  scheduled: "bg-blue-100 text-blue-700 border-blue-200",
  completed: "bg-emerald-100 text-emerald-700 border-emerald-200",
  cancelled: "bg-rose-100 text-rose-700 border-rose-200",
};

function formatDate(value) {
  try {
    return new Date(value).toLocaleString("es-PE", {
      dateStyle: "medium",
      timeStyle: "short",
    });
  } catch {
    return value;
  }
}

export default function Appointments() {
  const [appointments, setAppointments] = useState([]);
  const [pets, setPets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [updatingId, setUpdatingId] = useState(null);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm({
    defaultValues: {
      pet: "",
      scheduled_at: "",
      reason: "",
      notes: "",
      status: "scheduled",
    },
  });

  async function loadData() {
    setLoading(true);
    try {
      const [{ data: appointmentsData }, { data: petsData }] = await Promise.all([
        listAppointments(),
        listPets(),
      ]);
      setAppointments(appointmentsData);
      setPets(petsData);
    } catch (error) {
      console.error("Error cargando citas", error);
      setAppointments([]);
      if (error?.response?.status === 401) {
        toast.error("Inicia sesión para ver tus citas");
      } else {
        toast.error("No se pudieron obtener las citas");
      }
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  const onSubmit = async (formData) => {
    try {
      const payload = {
        pet: Number(formData.pet),
        scheduled_at: new Date(formData.scheduled_at).toISOString(),
        reason: formData.reason,
        status: formData.status || "scheduled",
        notes: formData.notes,
      };
      await createAppointment(payload);
      toast.success("Cita registrada");
      reset({ pet: "", scheduled_at: "", reason: "", notes: "", status: "scheduled" });
      loadData();
    } catch (error) {
      console.error("Error creando cita", error);
      toast.error("No se pudo registrar la cita");
    }
  };

  const handleStatusChange = async (id, status) => {
    setUpdatingId(`${id}-${status}`);
    try {
      await updateAppointment(id, { status });
      toast.success(`Cita marcada como ${STATUS_LABEL[status] || status}`);
      loadData();
    } catch (error) {
      console.error("Error actualizando cita", error);
      toast.error("No se pudo actualizar la cita");
    } finally {
      setUpdatingId(null);
    }
  };

  const sortedAppointments = useMemo(
    () =>
      [...appointments].sort((a, b) =>
        new Date(b.scheduled_at).getTime() - new Date(a.scheduled_at).getTime()
      ),
    [appointments]
  );

  const canCreate = pets.length > 0;

  return (
    <div className="grid lg:grid-cols-[3fr_2fr] gap-6">
      <section className="card p-6">
        <header className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-xl font-semibold">Citas</h1>
            <p className="text-sm text-gray-500">Revisa y gestiona tus próximas atenciones.</p>
          </div>
          <span className="text-sm text-gray-500">Total: {appointments.length}</span>
        </header>

        {loading ? (
          <p className="text-sm text-gray-500">Cargando citas...</p>
        ) : sortedAppointments.length === 0 ? (
          <p className="text-sm text-gray-500">No hay citas registradas.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead>
                <tr className="text-left text-gray-500 border-b">
                  <th className="py-2 pr-4">Mascota</th>
                  <th className="py-2 pr-4">Fecha</th>
                  <th className="py-2 pr-4">Motivo</th>
                  <th className="py-2 pr-4">Estado</th>
                  <th className="py-2 pr-4">Notas</th>
                  <th className="py-2 pr-4 text-right">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {sortedAppointments.map((appointment) => {
                  const key = `${appointment.id}-${appointment.status}`;
                  return (
                    <tr key={appointment.id} className="border-b last:border-0">
                      <td className="py-2 pr-4 font-medium">{appointment.pet_name || appointment.pet}</td>
                      <td className="py-2 pr-4 whitespace-nowrap">{formatDate(appointment.scheduled_at)}</td>
                      <td className="py-2 pr-4">{appointment.reason}</td>
                      <td className="py-2 pr-4">
                        <span
                          className={`inline-flex items-center gap-1 px-2 py-1 rounded-full border text-xs font-medium ${
                            statusTone[appointment.status] || "bg-gray-100 text-gray-600 border-gray-200"
                          }`}
                        >
                          {STATUS_LABEL[appointment.status] || appointment.status}
                        </span>
                      </td>
                      <td className="py-2 pr-4 text-gray-500">{appointment.notes || "—"}</td>
                      <td className="py-2 pr-0 text-right space-x-2">
                        {appointment.status === "scheduled" && (
                          <>
                            <Button
                              size="small"
                              variant="text"
                              color="success"
                              disabled={updatingId === `${appointment.id}-completed`}
                              onClick={() => handleStatusChange(appointment.id, "completed")}
                            >
                              Completar
                            </Button>
                            <Button
                              size="small"
                              variant="text"
                              color="error"
                              disabled={updatingId === `${appointment.id}-cancelled`}
                              onClick={() => handleStatusChange(appointment.id, "cancelled")}
                            >
                              Cancelar
                            </Button>
                          </>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="card p-6 space-y-4">
        <div>
          <h2 className="text-lg font-semibold">Agendar nueva cita</h2>
          <p className="text-sm text-gray-500">Completa el formulario para registrar una atención.</p>
        </div>

        {canCreate ? (
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <TextField
              select
              label="Mascota"
              size="small"
              fullWidth
              defaultValue=""
              error={Boolean(errors.pet)}
              helperText={errors.pet ? "Selecciona una mascota" : undefined}
              {...register("pet", { required: true })}
            >
              <MenuItem value="" disabled>
                Selecciona una mascota
              </MenuItem>
              {pets.map((pet) => (
                <MenuItem key={pet.id} value={pet.id}>
                  {pet.name} • {pet.species}
                </MenuItem>
              ))}
            </TextField>

            <TextField
              label="Fecha y hora"
              type="datetime-local"
              size="small"
              fullWidth
              InputLabelProps={{ shrink: true }}
              error={Boolean(errors.scheduled_at)}
              helperText={errors.scheduled_at ? "Indica la fecha de la cita" : ""}
              {...register("scheduled_at", { required: true })}
            />

            <TextField
              label="Motivo"
              size="small"
              fullWidth
              error={Boolean(errors.reason)}
              helperText={errors.reason ? "Describe el motivo" : ""}
              {...register("reason", { required: true })}
            />

            <TextField
              label="Notas (opcional)"
              size="small"
              fullWidth
              multiline
              minRows={2}
              {...register("notes")}
            />

            <input type="hidden" value="scheduled" {...register("status")} />

            <Button type="submit" variant="contained" fullWidth>
              Guardar cita
            </Button>
          </form>
        ) : (
          <div className="rounded-md bg-amber-50 border border-amber-200 text-amber-700 text-sm p-4">
            Registra primero una mascota para poder agendar citas.
          </div>
        )}
      </section>
    </div>
  );
}
