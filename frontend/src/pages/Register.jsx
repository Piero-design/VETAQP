import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import { TextField, Button, Grid } from "@mui/material";
import { registerUser } from "../api/userService";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";

const schema = yup.object({
  username: yup.string().min(3).required(),
  email: yup.string().email().required(),
  password: yup.string().min(6).required(),
  password2: yup.string().oneOf([yup.ref("password")], "No coincide"),
});

export default function Register() {
  const nav = useNavigate();
  const { register, handleSubmit, formState: { errors, isSubmitting }, reset, watch } = useForm({
    resolver: yupResolver(schema),
  });

  const onSubmit = async (data) => {
    await registerUser({ username: data.username, email: data.email, password: data.password });
    toast.success("Cuenta creada. Inicia sesión.");
    reset();
    nav("/login");
  };

  return (
    <div className="max-w-2xl mx-auto card p-6">
      <h1 className="text-2xl font-bold mb-4">Registro</h1>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField label="Usuario" fullWidth size="small" {...register("username")}
                       error={!!errors.username} helperText={errors.username?.message}/>
          </Grid>
          <Grid item xs={12}>
            <TextField label="Correo" fullWidth size="small" {...register("email")}
                       error={!!errors.email} helperText={errors.email?.message}/>
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField label="Contraseña" type="password" fullWidth size="small" {...register("password")}
                       error={!!errors.password} helperText={errors.password?.message}/>
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField label="Confirmar contraseña" type="password" fullWidth size="small" {...register("password2")}
                       error={!!errors.password2} helperText={errors.password2?.message}/>
          </Grid>
          <Grid item xs={12}>
            <Button type="submit" variant="contained" disabled={isSubmitting}>Registrarse</Button>
          </Grid>
        </Grid>
      </form>
    </div>
  );
}
