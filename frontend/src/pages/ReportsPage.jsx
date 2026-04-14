import { useState } from "react";
import api from "../api/client";

export default function ReportsPage() {
  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");
  const [report, setReport] = useState(null);

  const fetchReport = async () => {
    const { data } = await api.get("/reports", { params: { from_date: fromDate, to_date: toDate } });
    setReport(data);
  };

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold mb-4 text-slate-700">Reports</h2>
      <div className="card-soft p-4 flex flex-wrap gap-2">
        <input type="datetime-local" className="input-soft" value={fromDate} onChange={(e) => setFromDate(e.target.value)} />
        <input type="datetime-local" className="input-soft" value={toDate} onChange={(e) => setToDate(e.target.value)} />
        <button className="btn-primary" onClick={fetchReport}>
          Apply
        </button>
      </div>
      {report && (
        <div className="card-soft p-4">
          <p className="text-sm">Total Calls: {report.total_calls}</p>
          <p className="text-sm">Total Duration: {report.total_duration}s</p>
          <div className="mt-3">
            {report.agent_performance.map((a) => (
              <p key={a.agent_id} className="text-sm">
                Agent {a.agent_id}: {a.calls} calls / {a.duration}s
              </p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
