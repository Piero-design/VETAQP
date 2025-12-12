import api from "./axiosConfig";

export const createOrder = (orderData) => api.post("/orders/", orderData);
export const listOrders = () => api.get("/orders/");
export const getOrder = (id) => api.get(`/orders/${id}/`);
export const confirmPayment = (id) => api.post(`/orders/${id}/confirm_payment/`);
