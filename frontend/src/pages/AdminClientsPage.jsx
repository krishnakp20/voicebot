import { useEffect, useState } from "react";
import api from "../api/client";

const empty = {
  name: "",
  plan: "starter",
  admin_email: "",
  admin_name: "",
  admin_password: ""
};

export default function AdminClientsPage() {
  const [clients, setClients] = useState([]);
  const [form, setForm] = useState(empty);

  const load = () => api.get("/clients").then((res) => setClients(res.data));
  useEffect(() => {
    load();
  }, []);

  const submit = async (e) => {
    e.preventDefault();
    await api.post("/clients", form);
    setForm(empty);
    load();
  };

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold mb-4 text-slate-700">Client Management</h2>
      <form className="card-soft p-4 grid grid-cols-1 md:grid-cols-2 gap-3" onSubmit={submit}>
        {Object.keys(form).map((k) => (
          <input
            key={k}
            className="input-soft"
            value={form[k]}
            placeholder={k}
            onChange={(e) => setForm({ ...form, [k]: e.target.value })}
          />
        ))}
        <button className="col-span-1 md:col-span-2 btn-primary w-fit">Create Client</button>
      </form>
      <div className="card-soft overflow-x-auto">
        <table className="w-full table-soft">
          <thead className="bg-amber-50/50">
            <tr>
              <th className="p-3 text-left">Name</th>
              <th className="p-3 text-left">Plan</th>
              <th className="p-3 text-left">API Key</th>
              <th className="p-3 text-left">Status</th>
            </tr>
          </thead>
          <tbody>
            {clients.map((client) => (
              <tr key={client.id} className="border-t">
                <td className="p-3">{client.name}</td>
                <td className="p-3">{client.plan}</td>
                <td className="p-3">{client.api_key}</td>
                <td className="p-3">{client.is_enabled ? "Enabled" : "Disabled"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
