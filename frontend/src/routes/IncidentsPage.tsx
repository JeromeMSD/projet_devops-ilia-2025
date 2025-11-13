import { useState, useMemo } from "react";
import { mockIncidents } from "../mocks/mockData";

const padTwoDigits = (value: number) => value.toString().padStart(2, '0');

const formatIncidentDate = (timestamp: number) => {
    const date = new Date(timestamp * 1000);
    return `${padTwoDigits(date.getDate())}/${padTwoDigits(date.getMonth() + 1)}/${date.getFullYear()}, ${padTwoDigits(
        date.getHours(),
    )}:${padTwoDigits(date.getMinutes())}:${padTwoDigits(date.getSeconds())}`;
};

const PAGE_SIZE = 10; // nombre d'incidents par page

function IncidentsPage() {
  const [statusFilter, setStatusFilter] = useState<"all" | "open" | "resolved" | "mitigated">("all");
  const [sevFilter, setSevFilter] = useState<number | "all">("all");
  const [serviceFilter, setServiceFilter] = useState<string>("all");
  const [page, setPage] = useState(1);

  // Filtrer les incidents
  const filteredIncidents = useMemo(() => {
    return mockIncidents
      .filter((incident) => {
        const statusMatch = statusFilter === "all" || incident.status === statusFilter;
        const sevMatch = sevFilter === "all" || incident.sev === sevFilter;
        const serviceMatch =
          serviceFilter === "all" ||
          incident.services.some((s) => s.toLowerCase() === serviceFilter.toLowerCase());
        return statusMatch && sevMatch && serviceMatch;
      })
      .sort((a, b) => b.started_at - a.started_at); // tri par recence (plus récent en premier)
  }, [statusFilter, sevFilter, serviceFilter]);

  // Pagination
  const paginatedIncidents = useMemo(() => {
    const start = (page - 1) * PAGE_SIZE;
    return filteredIncidents.slice(start, start + PAGE_SIZE);
  }, [filteredIncidents, page]);

  const totalPages = Math.ceil(filteredIncidents.length / PAGE_SIZE);

  // Services uniques pour le filtre
  const allServices = Array.from(
    new Set(mockIncidents.flatMap((incident) => incident.services))
  );

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">Incidents récents</h1>

      {/* Filtres */}
      <div className="flex gap-4 mb-6 flex-wrap">
        <select
          className="border rounded px-3 py-1"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value as 'all' | 'open' | 'resolved' | 'mitigated')}
        >
          <option value="all">Tous les statuts</option>
          <option value="open">En cours</option>
          <option value="mitigated">Mitigé</option>
          <option value="resolved">Résolu</option>
        </select>

        <select
          className="border rounded px-3 py-1"
          value={sevFilter}
          onChange={(e) =>
            setSevFilter(e.target.value === "all" ? "all" : Number(e.target.value))
          }
        >
          <option value="all">Toutes sévérités</option>
          <option value="1">Sévérité 1</option>
          <option value="2">Sévérité 2</option>
          <option value="3">Sévérité 3</option>
          <option value="4">Sévérité 4</option>
        </select>

        <select
          className="border rounded px-3 py-1"
          value={serviceFilter}
          onChange={(e) => setServiceFilter(e.target.value)}
        >
          <option value="all">Tous les services</option>
          {allServices.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
      </div>

      {/* Liste d’incidents (défilement sur la page) */}
      <div className="space-y-4">
        {paginatedIncidents.map((incident) => (
          <div key={incident.id} className="border rounded p-4 shadow hover:shadow-lg transition">
            <div className="flex justify-between items-center mb-2">
              <h2 className="text-xl font-semibold">{incident.title}</h2>
              <span
                className={`px-2 py-1 rounded text-sm font-medium ${
                  incident.status === "open"
                    ? "bg-red-200 text-red-800"
                    : incident.status === "mitigated"
                    ? "bg-yellow-200 text-yellow-800"
                    : "bg-green-200 text-green-800"
                }`}
              >
                {incident.status}
              </span>
            </div>
            <p className="text-gray-700 mb-1">{incident.summary}</p>
            
            {/* Informations sur deux lignes */}
            <p className="text-gray-500 text-sm flex justify-between">
              <span>Services : {incident.services.join(", ")}</span>
              <span>Sévérité : {incident.sev}</span>
            </p>
            <p className="text-gray-500 text-sm flex justify-between">
              <span>Commandant : {incident.commander}</span>
              <span>Date : {formatIncidentDate(incident.started_at)}</span>
            </p>
          </div>
        ))}
      </div>

      {/* Pagination */}
      <div className="flex justify-between items-center mt-4">
        <button
          className="px-3 py-1 border rounded disabled:opacity-50"
          onClick={() => setPage((p) => Math.max(1, p - 1))}
          disabled={page === 1}
        >
          Précédent
        </button>
        <span>
          Page {page} / {totalPages || 1}
        </span>
        <button
          className="px-3 py-1 border rounded disabled:opacity-50"
          onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
          disabled={page === totalPages || totalPages === 0}
        >
          Suivant
        </button>
      </div>
    </div>
  );
}

export default IncidentsPage;
