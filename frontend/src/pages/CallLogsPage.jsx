import { useEffect, useState } from "react";
import api from "../api/client";

export default function CallLogsPage() {
  const [calls, setCalls] = useState([]);

  useEffect(() => {
    api.get("/calls").then((res) => setCalls(res.data));
  }, []);

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold mb-4 text-slate-700">Call Detail Records</h2>
      <div className="card-soft overflow-x-auto">
        <table className="w-full table-soft">
          <thead className="bg-amber-50/50">
            <tr>
              <th className="p-3 text-left">Call ID</th>
              <th className="p-3 text-left">Phone</th>
              <th className="p-3 text-left">Duration</th>
              <th className="p-3 text-left">Status</th>
            </tr>
          </thead>
          <tbody>
            {calls.map((call) => (
              <tr key={call.call_id} className="border-t">
                <td className="p-3">{call.call_id}</td>
                <td className="p-3">{call.phone_number}</td>
                <td className="p-3">{call.duration}s</td>
                <td className="p-3">{call.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
