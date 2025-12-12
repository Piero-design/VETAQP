import { Routes, Route, Navigate } from "react-router-dom";
import Home from "../pages/Home";
import Login from "../pages/Login";
import Register from "../pages/Register";
import Profile from "../pages/Profile";
import Pets from "../pages/Pets";
import Inventory from '../pages/Inventory';
import Payments from '../pages/Payments';
import Memberships from '../pages/Memberships';
import Orders from '../pages/Orders';
import Appointments from '../pages/Appointments';
import Notifications from '../pages/Notifications';
import Chat from '../pages/Chat';
import MedicalHistory from '../pages/MedicalHistory';
import OrderTracking from '../pages/OrderTracking';
import Dashboard from '../pages/Dashboard';

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/catalogo" element={<Home />} />
      <Route path="/citas" element={<Appointments />} />
      <Route path="/appointments" element={<Appointments />} />
      <Route path="/promos" element={<div className="card p-6">Promociones (MVP)</div>} />
      <Route path="/pets" element={<Pets />} />
      <Route path="/inventory" element={<Inventory />} />
      <Route path="/payments" element={<Payments />} />
      <Route path="/memberships" element={<Memberships />} />
      <Route path="/orders" element={<Orders />} />
      <Route path="/notifications" element={<Notifications />} />
      <Route path="/chat" element={<Chat />} />
      <Route path="/medical-history" element={<MedicalHistory />} />
      <Route path="/order-tracking" element={<OrderTracking />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}