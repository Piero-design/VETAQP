import api from "./axiosConfig";

export const getCategories = () => api.get("/products/categories/");
export const getSubCategories = () => api.get("/products/subcategories/");
export const getPetTypes = () => api.get("/products/pet-types/");
export const getProductsByCategory = (categoryId) => 
  api.get("/products/", { params: { category: categoryId } });
export const getProductsByPetType = (petTypeId) => 
  api.get("/products/", { params: { pet_type: petTypeId } });
