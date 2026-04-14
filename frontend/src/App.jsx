import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import Layout from "./components/Layout";
import AdminClientsPage from "./pages/AdminClientsPage";
import AgentsPage from "./pages/AgentsPage";
import BillingPage from "./pages/BillingPage";
import CallLogsPage from "./pages/CallLogsPage";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import RecordingsPage from "./pages/RecordingsPage";
import ReportsPage from "./pages/ReportsPage";

function Protected({ children }) {
  const token = localStorage.getItem("token");
  const location = useLocation();
  if (!token) return <Navigate to="/" state={{ from: location }} replace />;
  return <Layout>{children}</Layout>;
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/dashboard" element={<Protected><DashboardPage /></Protected>} />
      <Route path="/agents" element={<Protected><AgentsPage /></Protected>} />
      <Route path="/calls" element={<Protected><CallLogsPage /></Protected>} />
      <Route path="/recordings" element={<Protected><RecordingsPage /></Protected>} />
      <Route path="/reports" element={<Protected><ReportsPage /></Protected>} />
      <Route path="/billing" element={<Protected><BillingPage /></Protected>} />
      <Route path="/admin/clients" element={<Protected><AdminClientsPage /></Protected>} />
    </Routes>
  );
}
