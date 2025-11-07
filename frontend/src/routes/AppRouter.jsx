import { Routes, Route, Navigate } from "react-router-dom";
import Home from "../pages/Home";
import Login from "../pages/Login";
import Register from "../pages/Register";
import Profile from "../pages/Profile";
import Pets from "../pages/Pets";

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/catalogo" element={<Home />} />
      <Route path="/citas" element={<div className="card p-6">Citas (MVP)</div>} />
      <Route path="/promos" element={<div className="card p-6">Promociones (MVP)</div>} />
      <Route path="/pets" element={<Pets />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}
