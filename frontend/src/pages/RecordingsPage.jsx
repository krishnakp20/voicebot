import { useEffect, useState } from "react";
import api from "../api/client";

export default function RecordingsPage() {
  const [calls, setCalls] = useState([]);

  useEffect(() => {
    api.get("/calls").then((res) => setCalls(res.data.filter((c) => c.recording_url)));
  }, []);

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold mb-4 text-slate-700">Recordings</h2>
      <div className="space-y-3">
        {calls.map((call) => (
          <div key={call.call_id} className="card-soft p-4 flex justify-between">
            <span>{call.call_id}</span>
            <a className="text-blue-600" href={`${import.meta.env.VITE_API_BASE_URL}/calls/${call.call_id}/recording`}>
              Stream
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}
