import { useState, useEffect } from 'react';
import axios from 'axios';

const Appointments = () => {
  const [appointments, setAppointments] = useState([]);
  const [pets, setPets] = useState([]);
  const [filterStatus, setFilterStatus] = useState('');
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);

  // Estado del formulario
  const [selectedPet, setSelectedPet] = useState('');
  const [appointmentDate, setAppointmentDate] = useState('');
  const [appointmentTime, setAppointmentTime] = useState('');
  const [reason, setReason] = useState('');
  const [veterinarian, setVeterinarian] = useState('');
  const [notes, setNotes] = useState('');

  useEffect(() => {
    fetchAppointments();
    fetchPets();
  }, [filterStatus]);

  const fetchAppointments = async () => {
    try {
      const token = localStorage.getItem('access');
      const url = filterStatus 
        ? `http://localhost:8000/api/appointments/?status=${filterStatus}`
        : 'http://localhost:8000/api/appointments/';
      
      const response = await axios.get(url, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAppointments(response.data);
    } catch (error) {
      console.error('Error al cargar citas:', error);
    }
  };

  const fetchPets = async () => {
    try {
      const token = localStorage.getItem('access');
      const response = await axios.get('http://localhost:8000/api/pets/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPets(response.data);
    } catch (error) {
      console.error('Error al cargar mascotas:', error);
    }
  };

  const createAppointment = async (e) => {
    e.preventDefault();
    if (!selectedPet || !appointmentDate || !appointmentTime || !reason) {
      alert('Por favor completa todos los campos obligatorios');
      return;
    }

    setLoading(true);
    try {
      const token = localStorage.getItem('access');
      const appointmentData = {
        pet: parseInt(selectedPet),
        appointment_date: appointmentDate,
        appointment_time: appointmentTime,
        reason,
        veterinarian,
        notes
      };

      await axios.post('http://localhost:8000/api/appointments/', appointmentData, {
        headers: { Authorization: `Bearer ${token}` }
      });

      alert('Cita agendada exitosamente');
      setSelectedPet('');
      setAppointmentDate('');
      setAppointmentTime('');
      setReason('');
      setVeterinarian('');
      setNotes('');
      setShowForm(false);
      fetchAppointments();
    } catch (error) {
      console.error('Error al crear cita:', error);
      const errorMsg = error.response?.data?.appointment_date?.[0] || 
                       error.response?.data?.appointment_time?.[0] ||
                       error.response?.data?.pet?.[0] ||
                       'Error al agendar la cita';
      alert(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const cancelAppointment = async (id) => {
    if (!confirm('¿Estás seguro de cancelar esta cita?')) return;

    try {
      const token = localStorage.getItem('access');
      await axios.delete(`http://localhost:8000/api/appointments/${id}/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('Cita cancelada exitosamente');
      fetchAppointments();
    } catch (error) {
      console.error('Error al cancelar cita:', error);
      alert(error.response?.data?.detail || 'Error al cancelar la cita');
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      SCHEDULED: 'bg-blue-100 text-blue-800',
      CONFIRMED: 'bg-green-100 text-green-800',
      IN_PROGRESS: 'bg-purple-100 text-purple-800',
      COMPLETED: 'bg-gray-100 text-gray-800',
      CANCELLED: 'bg-red-100 text-red-800'
    };
    return badges[status] || 'bg-gray-100 text-gray-800';
  };

  const getStatusLabel = (status) => {
    const labels = {
      SCHEDULED: 'Programada',
      CONFIRMED: 'Confirmada',
      IN_PROGRESS: 'En Progreso',
      COMPLETED: 'Completada',
      CANCELLED: 'Cancelada'
    };
    return labels[status] || status;
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString + 'T00:00:00');
    return date.toLocaleDateString('es-ES', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatTime = (timeString) => {
    const [hours, minutes] = timeString.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const hour12 = hour % 12 || 12;
    return `${hour12}:${minutes} ${ampm}`;
  };

  // Filtrar citas próximas (no completadas ni canceladas)
  const upcomingAppointments = appointments.filter(
    app => !['COMPLETED', 'CANCELLED'].includes(app.status)
  );

  // Filtrar historial (completadas y canceladas)
  const pastAppointments = appointments.filter(
    app => ['COMPLETED', 'CANCELLED'].includes(app.status)
  );

  return (
    <div className="max-w-7xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Gestión de Citas</h1>

      {/* Botón Nueva Cita */}
      <div className="mb-6">
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-500 text-white px-6 py-3 rounded hover:bg-blue-600"
        >
          {showForm ? '✕ Cerrar Formulario' : '+ Nueva Cita'}
        </button>
      </div>

      {/* Formulario de Nueva Cita */}
      {showForm && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-2xl font-bold mb-4">Agendar Nueva Cita</h2>
          <form onSubmit={createAppointment} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Mascota *</label>
                <select
                  value={selectedPet}
                  onChange={(e) => setSelectedPet(e.target.value)}
                  className="w-full border rounded p-2"
                  required
                >
                  <option value="">Selecciona una mascota</option>
                  {pets.map(pet => (
                    <option key={pet.id} value={pet.id}>
                      {pet.name} ({pet.species})
                    </option>
                  ))}
                </select>
                {pets.length === 0 && (
                  <p className="text-sm text-red-600 mt-1">
                    Debes registrar una mascota primero
                  </p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Motivo de Consulta *</label>
                <input
                  type="text"
                  placeholder="Ej: Vacunación, Consulta general"
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                  className="w-full border rounded p-2"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Fecha *</label>
                <input
                  type="date"
                  value={appointmentDate}
                  onChange={(e) => setAppointmentDate(e.target.value)}
                  min={new Date().toISOString().split('T')[0]}
                  className="w-full border rounded p-2"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Hora * (8:00 AM - 8:00 PM)</label>
                <input
                  type="time"
                  value={appointmentTime}
                  onChange={(e) => setAppointmentTime(e.target.value)}
                  min="08:00"
                  max="20:00"
                  className="w-full border rounded p-2"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Veterinario (opcional)</label>
                <input
                  type="text"
                  placeholder="Dr. García"
                  value={veterinarian}
                  onChange={(e) => setVeterinarian(e.target.value)}
                  className="w-full border rounded p-2"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Notas adicionales (opcional)</label>
              <textarea
                placeholder="Información adicional sobre la cita"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                className="w-full border rounded p-2"
                rows="3"
              />
            </div>

            <button
              type="submit"
              disabled={loading || pets.length === 0}
              className="w-full bg-green-500 text-white py-3 rounded hover:bg-green-600 disabled:bg-gray-400"
            >
              {loading ? 'Agendando...' : 'Agendar Cita'}
            </button>
          </form>
        </div>
      )}

      {/* Filtros */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-bold mb-4">Filtrar Citas</h2>
        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
          className="border rounded p-2 w-full md:w-64"
        >
          <option value="">Todas las citas</option>
          <option value="SCHEDULED">Programadas</option>
          <option value="CONFIRMED">Confirmadas</option>
          <option value="IN_PROGRESS">En Progreso</option>
          <option value="COMPLETED">Completadas</option>
          <option value="CANCELLED">Canceladas</option>
        </select>
      </div>

      {/* Citas Próximas */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-2xl font-bold mb-4">
          📅 Próximas Citas ({upcomingAppointments.length})
        </h2>
        {upcomingAppointments.length === 0 ? (
          <p className="text-gray-500">No hay citas próximas</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {upcomingAppointments.map(app => (
              <div key={app.id} className="border rounded-lg p-4 hover:shadow-lg transition">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h3 className="font-bold text-lg">🐾 {app.pet_name}</h3>
                    <p className="text-sm text-gray-600">{app.pet_species}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusBadge(app.status)}`}>
                    {getStatusLabel(app.status)}
                  </span>
                </div>

                <div className="space-y-2 mb-3">
                  <p className="text-sm">
                    <span className="font-semibold">📆 Fecha:</span> {formatDate(app.appointment_date)}
                  </p>
                  <p className="text-sm">
                    <span className="font-semibold">🕐 Hora:</span> {formatTime(app.appointment_time)}
                  </p>
                  <p className="text-sm">
                    <span className="font-semibold">💊 Motivo:</span> {app.reason}
                  </p>
                  {app.veterinarian && (
                    <p className="text-sm">
                      <span className="font-semibold">👨‍⚕️ Veterinario:</span> {app.veterinarian}
                    </p>
                  )}
                  {app.notes && (
                    <p className="text-sm text-gray-600">
                      <span className="font-semibold">📝 Notas:</span> {app.notes}
                    </p>
                  )}
                  {app.is_today && (
                    <p className="text-sm font-bold text-green-600">
                      ⏰ ¡La cita es hoy!
                    </p>
                  )}
                </div>

                {app.status === 'SCHEDULED' && (
                  <button
                    onClick={() => cancelAppointment(app.id)}
                    className="w-full bg-red-500 text-white py-2 rounded hover:bg-red-600"
                  >
                    Cancelar Cita
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Historial */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold mb-4">
          📋 Historial ({pastAppointments.length})
        </h2>
        {pastAppointments.length === 0 ? (
          <p className="text-gray-500">No hay historial de citas</p>
        ) : (
          <div className="space-y-3">
            {pastAppointments.map(app => (
              <div key={app.id} className="border rounded-lg p-4 hover:shadow-md transition">
                <div className="flex justify-between items-center">
                  <div className="flex-1">
                    <h3 className="font-bold">🐾 {app.pet_name}</h3>
                    <p className="text-sm text-gray-600">
                      {formatDate(app.appointment_date)} - {formatTime(app.appointment_time)}
                    </p>
                    <p className="text-sm">💊 {app.reason}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusBadge(app.status)}`}>
                    {getStatusLabel(app.status)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Appointments;
