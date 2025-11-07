import api from "./axiosConfig";

export const register = (data) => api.post("/users/register/", data);
export const login = (data) => api.post("/users/login/", data);
export const getProfile = (token) =>
  api.get("/users/profile/", { headers: { Authorization: `Bearer ${token}` } });
