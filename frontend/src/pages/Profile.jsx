import { useEffect, useState } from "react";
import { getProfile } from "../api/userService";

export default function Profile() {
  const [user, setUser] = useState(null);
  useEffect(() => {
    (async () => {
      try { const { data } = await getProfile(); setUser(data); }
      catch { setUser(null); }
    })();
  }, []);
  if (!user) return <div className="card p-6">Inicia sesión para ver tu perfil.</div>;
  return (
    <div className="card p-6 max-w-lg">
      <h1 className="text-2xl font-bold mb-2">Hola, {user.username} 👋</h1>
      <p className="text-gray-600">Correo: {user.email || "—"}</p>
    </div>
  );
}
