// src/pages/Login.jsx

import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import { TextField, Checkbox, FormControlLabel, Button } from "@mui/material";
import { loginUser } from "../api/userService";
import { toast } from "react-toastify";
import { Link, useNavigate } from "react-router-dom";

const schema = yup.object({
  username: yup.string().required("Usuario requerido"),
  password: yup.string().required("Contraseña requerida"),
});

export default function Login() {
  const nav = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm({
    resolver: yupResolver(schema)
  });

  const onSubmit = async (data) => {
    try {
      const res = await loginUser(data);

      // *** TOKEN CORRECTO ***
      localStorage.setItem("access", res.data.access);

      toast.success("Inicio de sesión exitoso");
      nav("/profile");

    } catch (err) {
      toast.error("Credenciales inválidas");
    }
  };

  return (
    <div className="max-w-md mx-auto card p-6">
      <h1 className="text-2xl font-bold mb-4">Iniciar sesión</h1>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        
        <TextField
          label="Usuario"
          fullWidth
          size="small"
          {...register("username")}
          error={!!errors.username}
          helperText={errors.username?.message}
        />

        <TextField
          label="Contraseña"
          type="password"
          fullWidth
          size="small"
          {...register("password")}
          error={!!errors.password}
          helperText={errors.password?.message}
        />

        <FormControlLabel control={<Checkbox />} label="Recuérdame" />

        <Button type="submit" variant="contained" disabled={isSubmitting}>
          Ingresar
        </Button>
      </form>

      <div className="text-center text-sm mt-4">
        ¿No tienes cuenta?
        <Link to="/register" className="text-brand hover:underline">
          Registrarse
        </Link>
      </div>
    </div>
  );
}
