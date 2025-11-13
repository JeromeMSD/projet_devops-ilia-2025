export interface MockIncident {
  id: string;
  title: string;
  sev: number;
  services: string[];
  summary: string;
  status: "open" | "mitigated" | "resolved";
  started_at: number;
  commander: string;
}

export const mockIncidents: MockIncident[] = [
  {
    id: "INC-001",
    title: "Panne de la base de données principale",
    sev: 1,
    services: ["db", "backend"],
    summary: "La base de données principale ne répond plus.",
    status: "open",
    started_at: 1730073600,
    commander: "f6c74e13-8b4a-4b63-bf58-1c59a0c21840",
  },
  {
    id: "INC-002",
    title: "Latence API Europe",
    sev: 2,
    services: ["api"],
    summary: "Les temps de réponse API dépassaient 2s en EU-West.",
    status: "resolved",
    started_at: 1730077200,
    commander: "a3d11f92-4b76-46c0-9e83-6f23a28c91a0",
  },
  {
    id: "INC-003",
    title: "Problème de cache CDN",
    sev: 3,
    services: ["cdn"],
    summary: "Le cache CDN renvoyait des versions obsolètes.",
    status: "mitigated",
    started_at: 1730080800,
    commander: "d1a2f901-3e4b-45d8-b19b-5b12a943ef54",
  },
];
