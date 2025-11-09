export interface MockUser {
    id_user: string;
    firstname: string;
    lastname: string;
    email: string;
    role: string;
}

export const mockUser: MockUser = {
    id_user: "user-123-abc",
    firstname: "Sebastien",
    lastname: "Lacroix",
    email: "Sebastien.lacroix@projetdevops.com",
    role: "SRE"
};