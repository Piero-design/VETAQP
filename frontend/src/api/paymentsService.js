import api from "./axiosConfig";

export const listPayments = (params = {}) => api.get("/payments/", { params });
export const createPayment = (data) => api.post("/payments/", data);
export const updatePayment = (id, data) => api.patch(`/payments/${id}/`, data);
