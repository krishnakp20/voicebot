import { useState } from "react";
import { Link, useLocation } from "react-router-dom";

const nav = [
  { to: "/dashboard", label: "Dashboard", icon: "dashboard" },
  { to: "/agents", label: "Agents", icon: "agents" },
  { to: "/calls", label: "Call Logs", icon: "calls" },
  { to: "/recordings", label: "Recordings", icon: "recordings" },
  { to: "/reports", label: "Reports", icon: "reports" },
  { to: "/billing", label: "Billing", icon: "billing" },
  { to: "/admin/clients", label: "Admin Clients", icon: "clients" }
];

function NavIcon({ type }) {
  if (type === "dashboard") {
    return (
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="nav-icon" aria-hidden="true">
        <rect width="7" height="9" x="3" y="3" rx="1"></rect>
        <rect width="7" height="5" x="14" y="3" rx="1"></rect>
        <rect width="7" height="9" x="14" y="12" rx="1"></rect>
        <rect width="7" height="5" x="3" y="16" rx="1"></rect>
      </svg>
    );
  }
  if (type === "agents") {
    return (
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="nav-icon" aria-hidden="true">
        <path d="M12 8V4H8"></path>
        <rect width="16" height="12" x="4" y="8" rx="2"></rect>
        <path d="M2 14h2"></path>
        <path d="M20 14h2"></path>
      </svg>
    );
  }
  if (type === "calls") {
    return (
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="nav-icon" aria-hidden="true">
        <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.78 19.78 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.78 19.78 0 0 1 2.08 4.18 2 2 0 0 1 4.06 2h3a2 2 0 0 1 2 1.72c.12.9.33 1.78.62 2.62a2 2 0 0 1-.45 2.11L8 9.59a16 16 0 0 0 6.41 6.41l1.14-1.23a2 2 0 0 1 2.11-.45c.84.29 1.72.5 2.62.62A2 2 0 0 1 22 16.92z"></path>
      </svg>
    );
  }
  if (type === "recordings") {
    return (
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="nav-icon" aria-hidden="true">
        <circle cx="12" cy="12" r="10"></circle>
        <circle cx="12" cy="12" r="3"></circle>
      </svg>
    );
  }
  if (type === "reports") {
    return (
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="nav-icon" aria-hidden="true">
        <line x1="12" x2="12" y1="20" y2="10"></line>
        <line x1="18" x2="18" y1="20" y2="4"></line>
        <line x1="6" x2="6" y1="20" y2="16"></line>
      </svg>
    );
  }
  if (type === "billing") {
    return (
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="nav-icon" aria-hidden="true">
        <rect x="2" y="5" width="20" height="14" rx="2"></rect>
        <line x1="2" x2="22" y1="10" y2="10"></line>
      </svg>
    );
  }
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="nav-icon" aria-hidden="true">
      <path d="M16 20V4a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v16"></path>
      <rect width="20" height="14" x="2" y="6" rx="2"></rect>
    </svg>
  );
}

export default function Layout({ children }) {
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    window.location.href = "/";
  };

  return (
    <div className="min-h-screen app-bg p-4">
      <div className="flex gap-4 min-h-[calc(100vh-32px)]">
        <aside className={`${sidebarOpen ? "block" : "hidden"} w-64 panel border-soft rounded-2xl p-4`}>
          <h1 className="text-xl font-semibold mb-6 text-slate-700">Voice SaaS</h1>
          <nav className="space-y-2">
            {nav.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                className={`nav-link px-3 py-2 rounded-xl text-sm transition ${
                  location.pathname === item.to
                    ? "bg-indigo-100 text-indigo-800 border border-indigo-200"
                    : "text-slate-600 hover:bg-slate-100"
                }`}
              >
                <NavIcon type={item.icon} />
                {item.label}
              </Link>
            ))}
          </nav>
        </aside>
        <main className="flex-1 panel border-soft rounded-2xl">
          <div className="h-14 border-b border-soft px-5 flex items-center justify-between">
            <button
              type="button"
              className="menu-icon-btn"
              aria-label="Menu"
              onClick={() => setSidebarOpen((prev) => !prev)}
            >
              {sidebarOpen ? "✕" : "☰"}
            </button>
            <button type="button" className="btn-danger" onClick={logout}>
              Logout
            </button>
          </div>
          <div className="p-6">{children}</div>
        </main>
      </div>
    </div>
  );
}
