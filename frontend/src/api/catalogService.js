import api from "./axiosConfig";
export const listProducts = () => api.get("/products/");
export const listPets     = () => api.get("/pets/");
export const createPet    = (pet) => api.post("/pets/", pet);
