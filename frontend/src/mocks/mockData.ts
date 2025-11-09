export interface MockUser {
    id_user: string;
    firstname: string;
    lastname: string;
    email: string;
    role: string;
}

export const mockUser = {
    user_id: "user-123-abc",
    username: "Sebastien Lacroix",
    email: "seb.lacroix@test.com",
    role: "sre",
    created_at: "..."
};
export const mockIncidents = [
    { id: "inc-001", title: "Serveur de connexion inaccessible" },
    { id: "inc-002", title: "Latence sur l'API des paiements" }
];