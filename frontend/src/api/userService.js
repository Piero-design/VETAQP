import api from "./axiosConfig";

export const registerUser = (data) => api.post("/users/register/", data);
export const loginUser = (data) => api.post("/auth/login/", data);

// ✔ Evita 403 cuando no hay token
export const getProfile = () => {
  const token = localStorage.getItem("access");

  if (!token) {
    return Promise.reject({ noAuth: true });
  }

  return api.get("/users/me/");
};
