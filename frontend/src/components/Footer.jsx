export default function Footer() {
  return (
    <footer className="border-t bg-white">
      <div className="max-w-7xl mx-auto px-4 py-6 text-sm text-gray-600 flex flex-col sm:flex-row justify-between gap-2">
        <p>© {new Date().getFullYear()} AqpVet — Hecho con ❤️</p>
        <p>UNSA – Proyecto académico</p>
      </div>
    </footer>
  );
}
