import api from "./axiosConfig";

export const listAppointments = () => api.get("/appointments/");
export const createAppointment = (payload) => api.post("/appointments/", payload);
export const updateAppointment = (id, payload) => api.patch(`/appointments/${id}/`, payload);
