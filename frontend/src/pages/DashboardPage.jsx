import { useEffect, useState } from "react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import api from "../api/client";

const COLORS = ["#6366f1", "#22c55e", "#f59e0b", "#f43f5e", "#06b6d4"];

export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [calls, setCalls] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.get("/dashboard/stats"), api.get("/calls")])
      .then(([statsRes, callsRes]) => {
        setStats(statsRes.data);
        setCalls(callsRes.data || []);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="space-y-4">
        <div className="h-8 w-64 rounded bg-slate-200 animate-pulse" />
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-28 rounded-2xl bg-slate-200 animate-pulse" />
          ))}
        </div>
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
          <div className="h-80 rounded-2xl bg-slate-200 animate-pulse xl:col-span-2" />
          <div className="h-80 rounded-2xl bg-slate-200 animate-pulse" />
        </div>
      </div>
    );
  }

  if (!stats) return <p>Unable to load dashboard.</p>;

  const pieData = [
    { name: "Success", value: Number(stats.call_success_rate || 0) },
    { name: "Other", value: 100 - Number(stats.call_success_rate || 0) }
  ];

  const byDayMap = new Map();
  calls.forEach((call) => {
    const date = new Date(call.start_time);
    const key = Number.isNaN(date.getTime()) ? "N/A" : date.toLocaleDateString("en-GB", { day: "2-digit", month: "short" });
    const existing = byDayMap.get(key) || { day: key, calls: 0, duration: 0 };
    existing.calls += 1;
    existing.duration += Number(call.duration || 0);
    byDayMap.set(key, existing);
  });
  const callTrend = Array.from(byDayMap.values()).slice(-7);

  const statusMap = new Map();
  calls.forEach((call) => {
    const key = call.status || "unknown";
    statusMap.set(key, (statusMap.get(key) || 0) + 1);
  });
  const statusData = Array.from(statusMap.entries()).map(([status, total]) => ({ status, total }));

  const agentMap = new Map();
  calls.forEach((call) => {
    const key = `Agent ${call.agent_id}`;
    agentMap.set(key, (agentMap.get(key) || 0) + Number(call.duration || 0));
  });
  const agentDurationData = Array.from(agentMap.entries())
    .map(([agent, duration]) => ({ agent, duration }))
    .sort((a, b) => b.duration - a.duration)
    .slice(0, 5);

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h2 className="text-2xl font-semibold text-slate-800">Client Dashboard</h2>
        <span className="text-xs px-3 py-1 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-100">
          Live Analytics
        </span>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-4">
        {[
          ["Total Calls", stats.total_calls],
          ["Total Duration", `${stats.total_duration}s`],
          ["Active Agents", stats.active_agents],
          ["Success Rate", `${stats.call_success_rate}%`],
          ["Cost Usage", `$${stats.cost_usage}`]
        ].map(([title, value], idx) => (
          <div key={title} className="stat-card p-4">
            <p className="text-slate-500 text-sm">{title}</p>
            <p className="text-2xl font-semibold text-slate-800 mt-2">{value}</p>
            <div className="mt-3 h-1.5 rounded-full bg-slate-100 overflow-hidden">
              <div className="h-full rounded-full" style={{ width: `${65 + idx * 7}%`, background: COLORS[idx] }} />
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
        <div className="card-soft p-4 xl:col-span-2">
          <h3 className="font-semibold mb-3 text-slate-700">Call Volume Trend</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={callTrend}>
                <defs>
                  <linearGradient id="trendFill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.35} />
                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="day" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Area type="monotone" dataKey="calls" stroke="#6366f1" fill="url(#trendFill)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card-soft p-4">
          <h3 className="font-semibold mb-3 text-slate-700">Call Success Breakdown</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} dataKey="value" innerRadius={55} outerRadius={88} paddingAngle={2}>
                  {pieData.map((entry, idx) => (
                    <Cell key={entry.name} fill={COLORS[idx]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
        <div className="card-soft p-4">
          <h3 className="font-semibold mb-3 text-slate-700">Calls by Status</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={statusData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="status" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="total" fill="#22c55e" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="card-soft p-4">
          <h3 className="font-semibold mb-3 text-slate-700">Top Agent Duration</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={agentDurationData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis type="number" tick={{ fontSize: 12 }} />
                <YAxis type="category" dataKey="agent" width={80} tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="duration" fill="#0ea5e9" radius={[0, 8, 8, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
