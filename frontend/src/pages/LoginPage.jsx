import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/client";

export default function LoginPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const login = async (e) => {
    e.preventDefault();
    try {
      const { data } = await api.post("/auth/login", form);
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("role", data.role);
      navigate("/dashboard");
    } catch {
      setError("Login failed");
    }
  };

  return (
    <div className="min-h-screen app-bg p-4 md:p-8">
      <div className="max-w-5xl mx-auto min-h-[calc(100vh-32px)] md:min-h-[calc(100vh-64px)] grid grid-cols-1 lg:grid-cols-2 rounded-3xl overflow-hidden border-soft shadow-lg">
        <div className="hidden lg:flex login-hero p-10 flex-col justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-indigo-200 mb-3">AI Voice Platform</p>
            <h1 className="text-4xl font-semibold text-white leading-tight">
              Smart Calling
              <br />
              For Every Tenant
            </h1>
            <p className="text-indigo-100 mt-4 text-sm">
              Unified dashboard for calls, agents, analytics, and billing with role-based access.
            </p>
          </div>
          <div className="text-indigo-100 text-sm">Secure | Scalable | Multi-tenant</div>
        </div>

        <div className="panel p-8 md:p-10 flex items-center">
          <form className="w-full max-w-md mx-auto" onSubmit={login}>
            <p className="text-xs uppercase tracking-wider text-indigo-600 font-medium mb-2">Welcome back</p>
            <h2 className="text-3xl font-semibold text-slate-800 mb-2">Sign in</h2>
            <p className="text-sm text-slate-600 mb-6">Enter your credentials to continue.</p>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
                <input
                  className="input-soft w-full"
                  placeholder="admin@voicebot.local"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Password</label>
                <div className="relative">
                  <input
                    className="input-soft w-full pr-16"
                    placeholder="Enter password"
                    type={showPassword ? "text" : "password"}
                    value={form.password}
                    onChange={(e) => setForm({ ...form, password: e.target.value })}
                  />
                  <button
                    type="button"
                    className="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-indigo-600 hover:text-indigo-800"
                    onClick={() => setShowPassword((prev) => !prev)}
                  >
                    {showPassword ? "Hide" : "Show"}
                  </button>
                </div>
              </div>
            </div>

            {error && <p className="text-rose-600 text-sm mt-3">{error}</p>}

            <button className="w-full btn-primary text-sm py-2.5 mt-6">Login to Dashboard</button>
          </form>
        </div>
      </div>
    </div>
  );
}
