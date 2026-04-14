import { useEffect, useState } from "react";
import api from "../api/client";

const empty = {
  agent_name: "",
  prompt: "",
  welcome_message: "",
  voice: "",
  language: "en"
};

export default function AgentsPage() {
  const [agents, setAgents] = useState([]);
  const [form, setForm] = useState(empty);

  const load = () => api.get("/agents").then((res) => setAgents(res.data));
  useEffect(() => {
    load();
  }, []);

  const create = async (e) => {
    e.preventDefault();
    await api.post("/agents", form);
    setForm(empty);
    load();
  };

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold mb-4 text-slate-700">Agents</h2>
      <form className="card-soft p-4 grid grid-cols-1 md:grid-cols-2 gap-3" onSubmit={create}>
        {Object.keys(form).map((key) => (
          <input
            key={key}
            className="input-soft"
            placeholder={key}
            value={form[key]}
            onChange={(e) => setForm({ ...form, [key]: e.target.value })}
          />
        ))}
        <button className="col-span-1 md:col-span-2 btn-primary w-fit">Create Agent</button>
      </form>
      <div className="card-soft overflow-x-auto">
        <table className="w-full table-soft">
          <thead className="bg-amber-50/50">
            <tr>
              <th className="text-left p-3">Name</th>
              <th className="text-left p-3">Voice</th>
              <th className="text-left p-3">Language</th>
            </tr>
          </thead>
          <tbody>
            {agents.map((a) => (
              <tr key={a.id} className="border-t">
                <td className="p-3">{a.agent_name}</td>
                <td className="p-3">{a.voice}</td>
                <td className="p-3">{a.language}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
