export interface MockIncident {
    id: string;
    title: string;
    severity: 'critique' | 'majeure' | 'mineure'; 
    assignee_id?: string; 
}
export interface MockUser {
    user_id: string;
    username: string;
    email: string;
    role: 'user' | 'sre' | 'admin';
    created_at: string;
}
export const mockUser: MockUser = {
    user_id: "user-123-abc",
    username: "Sebastien Lacroix",
    email: "seb.lacroix@test.com",
    role: "sre",
    created_at: "2025-01-01"
};
export const mockIncidents: MockIncident[] = [
    { id: "inc-001", title: "Serveur de connexion inaccessible", severity: "majeure" }, 
    { id: "inc-002", title: "Latence sur l'API des paiements", severity: "mineure" },
    { id: "inc-003", title: "Défaut de base de données", severity: "critique" },
];