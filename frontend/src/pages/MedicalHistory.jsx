import { useState, useEffect } from 'react';
import axios from 'axios';

function MedicalHistory() {
  const [pets, setPets] = useState([]);
  const [selectedPet, setSelectedPet] = useState(null);
  const [medicalHistory, setMedicalHistory] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showRecordModal, setShowRecordModal] = useState(false);
  const [showVaccineModal, setShowVaccineModal] = useState(false);
  const [isStaff, setIsStaff] = useState(false);

  const [recordForm, setRecordForm] = useState({
    date: new Date().toISOString().split('T')[0],
    diagnosis: '',
    treatment: '',
    veterinarian: '',
    notes: '',
    weight: '',
    temperature: ''
  });

  const [vaccineForm, setVaccineForm] = useState({
    vaccine_name: '',
    date_administered: new Date().toISOString().split('T')[0],
    next_dose_date: '',
    veterinarian: '',
    batch_number: '',
    notes: ''
  });

  useEffect(() => {
    fetchPets();
    checkUserRole();
  }, []);

  const checkUserRole = async () => {
    try {
      const token = localStorage.getItem('access');
      const response = await axios.get('http://localhost:8000/api/auth/profile/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setIsStaff(response.data.is_staff);
    } catch (error) {
      console.error('Error checking user role:', error);
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
      console.error('Error fetching pets:', error);
      setError('Error al cargar las mascotas');
    }
  };

  const fetchMedicalHistory = async (petId) => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('access');
      const response = await axios.get(`http://localhost:8000/api/pets/${petId}/medical-history/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMedicalHistory(response.data);
    } catch (error) {
      console.error('Error fetching medical history:', error);
      setError('Error al cargar el historial médico');
    } finally {
      setLoading(false);
    }
  };

  const handlePetSelect = (pet) => {
    setSelectedPet(pet);
    fetchMedicalHistory(pet.id);
  };

  const handleCreateRecord = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('access');
      await axios.post('http://localhost:8000/api/pets/medical-records/', 
        { ...recordForm, pet: selectedPet.id },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setShowRecordModal(false);
      setRecordForm({
        date: new Date().toISOString().split('T')[0],
        diagnosis: '',
        treatment: '',
        veterinarian: '',
        notes: '',
        weight: '',
        temperature: ''
      });
      fetchMedicalHistory(selectedPet.id);
    } catch (error) {
      console.error('Error creating medical record:', error);
      alert('Error al crear el registro médico');
    }
  };

  const handleCreateVaccine = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('access');
      await axios.post('http://localhost:8000/api/pets/vaccines/', 
        { ...vaccineForm, pet: selectedPet.id },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setShowVaccineModal(false);
      setVaccineForm({
        vaccine_name: '',
        date_administered: new Date().toISOString().split('T')[0],
        next_dose_date: '',
        veterinarian: '',
        batch_number: '',
        notes: ''
      });
      fetchMedicalHistory(selectedPet.id);
    } catch (error) {
      console.error('Error creating vaccine:', error);
      alert('Error al registrar la vacuna');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Historial Médico</h1>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Lista de mascotas */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow p-4">
            <h2 className="text-xl font-semibold mb-4">Mis Mascotas</h2>
            {pets.length === 0 ? (
              <p className="text-gray-500">No tienes mascotas registradas</p>
            ) : (
              <div className="space-y-2">
                {pets.map(pet => (
                  <button
                    key={pet.id}
                    onClick={() => handlePetSelect(pet)}
                    className={`w-full text-left p-3 rounded-lg transition ${
                      selectedPet?.id === pet.id
                        ? 'bg-blue-100 border-2 border-blue-500'
                        : 'bg-gray-50 hover:bg-gray-100'
                    }`}
                  >
                    <div className="font-semibold">{pet.name}</div>
                    <div className="text-sm text-gray-600">{pet.species}</div>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Historial médico */}
        <div className="lg:col-span-3">
          {!selectedPet ? (
            <div className="bg-white rounded-lg shadow p-8 text-center">
              <p className="text-gray-500">Selecciona una mascota para ver su historial médico</p>
            </div>
          ) : loading ? (
            <div className="bg-white rounded-lg shadow p-8 text-center">
              <p>Cargando historial...</p>
            </div>
          ) : error ? (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          ) : medicalHistory ? (
            <div className="space-y-6">
              {/* Información de la mascota */}
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-2xl font-bold mb-2">{medicalHistory.name}</h2>
                <div className="grid grid-cols-2 gap-4 text-gray-600">
                  <div><span className="font-semibold">Especie:</span> {medicalHistory.species}</div>
                  <div><span className="font-semibold">Edad:</span> {medicalHistory.age} años</div>
                  <div><span className="font-semibold">Propietario:</span> {medicalHistory.owner_username}</div>
                </div>
              </div>

              {/* Registros médicos */}
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-xl font-bold">Registros Médicos</h3>
                  {isStaff && (
                    <button
                      onClick={() => setShowRecordModal(true)}
                      className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                    >
                      Nuevo Registro
                    </button>
                  )}
                </div>
                {medicalHistory.medical_records.length === 0 ? (
                  <p className="text-gray-500">No hay registros médicos</p>
                ) : (
                  <div className="space-y-4">
                    {medicalHistory.medical_records.map(record => (
                      <div key={record.id} className="border-l-4 border-blue-500 pl-4 py-2">
                        <div className="flex justify-between items-start mb-2">
                          <div>
                            <div className="font-semibold text-lg">{record.diagnosis}</div>
                            <div className="text-sm text-gray-600">{formatDate(record.date)}</div>
                          </div>
                          <div className="text-sm text-gray-600">Dr. {record.veterinarian}</div>
                        </div>
                        <div className="mt-2">
                          <div className="font-semibold">Tratamiento:</div>
                          <p className="text-gray-700">{record.treatment}</p>
                        </div>
                        {record.notes && (
                          <div className="mt-2">
                            <div className="font-semibold">Notas:</div>
                            <p className="text-gray-700">{record.notes}</p>
                          </div>
                        )}
                        <div className="flex gap-4 mt-2 text-sm text-gray-600">
                          {record.weight && <span>Peso: {record.weight} kg</span>}
                          {record.temperature && <span>Temperatura: {record.temperature} °C</span>}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Vacunas */}
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-xl font-bold">Vacunas</h3>
                  {isStaff && (
                    <button
                      onClick={() => setShowVaccineModal(true)}
                      className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
                    >
                      Registrar Vacuna
                    </button>
                  )}
                </div>
                {medicalHistory.vaccines.length === 0 ? (
                  <p className="text-gray-500">No hay vacunas registradas</p>
                ) : (
                  <div className="overflow-x-auto">
                    <table className="min-w-full">
                      <thead>
                        <tr className="bg-gray-50">
                          <th className="px-4 py-2 text-left">Vacuna</th>
                          <th className="px-4 py-2 text-left">Fecha</th>
                          <th className="px-4 py-2 text-left">Próxima Dosis</th>
                          <th className="px-4 py-2 text-left">Veterinario</th>
                          <th className="px-4 py-2 text-left">Lote</th>
                        </tr>
                      </thead>
                      <tbody>
                        {medicalHistory.vaccines.map(vaccine => (
                          <tr key={vaccine.id} className="border-b">
                            <td className="px-4 py-3 font-semibold">{vaccine.vaccine_name}</td>
                            <td className="px-4 py-3">{formatDate(vaccine.date_administered)}</td>
                            <td className="px-4 py-3">
                              {vaccine.next_dose_date ? (
                                <span className={vaccine.is_next_dose_pending ? 'text-orange-600 font-semibold' : ''}>
                                  {formatDate(vaccine.next_dose_date)}
                                </span>
                              ) : (
                                <span className="text-gray-400">-</span>
                              )}
                            </td>
                            <td className="px-4 py-3">Dr. {vaccine.veterinarian}</td>
                            <td className="px-4 py-3 text-sm text-gray-600">{vaccine.batch_number || '-'}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </div>
          ) : null}
        </div>
      </div>

      {/* Modal para nuevo registro médico */}
      {showRecordModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">Nuevo Registro Médico</h2>
            <form onSubmit={handleCreateRecord} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Fecha</label>
                <input
                  type="date"
                  value={recordForm.date}
                  onChange={(e) => setRecordForm({...recordForm, date: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Diagnóstico</label>
                <textarea
                  value={recordForm.diagnosis}
                  onChange={(e) => setRecordForm({...recordForm, diagnosis: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                  rows="3"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Tratamiento</label>
                <textarea
                  value={recordForm.treatment}
                  onChange={(e) => setRecordForm({...recordForm, treatment: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                  rows="3"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Veterinario</label>
                <input
                  type="text"
                  value={recordForm.veterinarian}
                  onChange={(e) => setRecordForm({...recordForm, veterinarian: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                  required
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Peso (kg)</label>
                  <input
                    type="number"
                    step="0.01"
                    value={recordForm.weight}
                    onChange={(e) => setRecordForm({...recordForm, weight: e.target.value})}
                    className="w-full border rounded px-3 py-2"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Temperatura (°C)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={recordForm.temperature}
                    onChange={(e) => setRecordForm({...recordForm, temperature: e.target.value})}
                    className="w-full border rounded px-3 py-2"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Notas adicionales</label>
                <textarea
                  value={recordForm.notes}
                  onChange={(e) => setRecordForm({...recordForm, notes: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                  rows="2"
                />
              </div>
              <div className="flex gap-2 justify-end">
                <button
                  type="button"
                  onClick={() => setShowRecordModal(false)}
                  className="px-4 py-2 border rounded hover:bg-gray-100"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Guardar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal para nueva vacuna */}
      {showVaccineModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">Registrar Vacuna</h2>
            <form onSubmit={handleCreateVaccine} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Nombre de la vacuna</label>
                <input
                  type="text"
                  value={vaccineForm.vaccine_name}
                  onChange={(e) => setVaccineForm({...vaccineForm, vaccine_name: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Fecha de aplicación</label>
                <input
                  type="date"
                  value={vaccineForm.date_administered}
                  onChange={(e) => setVaccineForm({...vaccineForm, date_administered: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Próxima dosis (opcional)</label>
                <input
                  type="date"
                  value={vaccineForm.next_dose_date}
                  onChange={(e) => setVaccineForm({...vaccineForm, next_dose_date: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Veterinario</label>
                <input
                  type="text"
                  value={vaccineForm.veterinarian}
                  onChange={(e) => setVaccineForm({...vaccineForm, veterinarian: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Número de lote (opcional)</label>
                <input
                  type="text"
                  value={vaccineForm.batch_number}
                  onChange={(e) => setVaccineForm({...vaccineForm, batch_number: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Notas (opcional)</label>
                <textarea
                  value={vaccineForm.notes}
                  onChange={(e) => setVaccineForm({...vaccineForm, notes: e.target.value})}
                  className="w-full border rounded px-3 py-2"
                  rows="2"
                />
              </div>
              <div className="flex gap-2 justify-end">
                <button
                  type="button"
                  onClick={() => setShowVaccineModal(false)}
                  className="px-4 py-2 border rounded hover:bg-gray-100"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                >
                  Guardar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default MedicalHistory;
