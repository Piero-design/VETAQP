import api from "./axiosConfig";
export const registerUser = (data) => api.post("/users/register/", data);
export const loginUser = (data) => api.post("/auth/login/", data);
export const getProfile  = () => api.get("/users/me/");
