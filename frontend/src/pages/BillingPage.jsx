import { useEffect, useState } from "react";
import api from "../api/client";

export default function BillingPage() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    api.get("/billing").then((res) => setItems(res.data));
  }, []);

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold mb-4 text-slate-700">Billing</h2>
      <div className="card-soft overflow-x-auto">
        <table className="w-full table-soft">
          <thead className="bg-amber-50/50">
            <tr>
              <th className="p-3 text-left">Month</th>
              <th className="p-3 text-left">Call Cost</th>
              <th className="p-3 text-left">OpenAI Cost</th>
              <th className="p-3 text-left">Sarvam Cost</th>
              <th className="p-3 text-left">Total</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={`${item.client_id}-${item.month}`} className="border-t">
                <td className="p-3">{item.month}</td>
                <td className="p-3">${item.call_cost}</td>
                <td className="p-3">${item.openai_cost}</td>
                <td className="p-3">${item.sarvam_cost}</td>
                <td className="p-3 font-semibold">${item.total_cost}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
