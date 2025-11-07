import { BrowserRouter } from "react-router-dom";
import AppRouter from "./routes/AppRouter";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./styles/index.css";

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-1 max-w-7xl mx-auto w-full px-4 py-6">
          <AppRouter />
        </main>
        <Footer />
      </div>
      <ToastContainer position="top-right" autoClose={2500} />
    </BrowserRouter>
  );
}
