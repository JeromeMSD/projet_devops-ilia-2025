import { render, screen } from '@testing-library/react';
import { vi } from 'vitest';
import type { AuthUser } from '@/auth/types.ts';
import ProfilePage from './ProfilePage';

const mockAuthUser: AuthUser = {
    id_user: 'user-123-abc',
    firstname: 'Sebastien',
    lastname: 'Lacroix',
    email: 'seb.lacroix@test.com',
    role: 'SRE',
    created_at: '2025-01-01T00:00:00.000Z',
};

vi.mock('react-auth-kit/hooks/useAuthUser', () => ({
    default: () => mockAuthUser,
}));

vi.mock('../mocks/mockData', () => ({
    mockUser: {
        username: 'Sebastien Lacroix',
        email: 'seb.lacroix@test.com',
        role: 'sre',
    },
    mockIncidents: [
        { id: 'inc-001', title: 'Serveur de connexion inaccessible' },
        { id: 'inc-002', title: 'Latence sur l\'API des paiements' },
    ],
}));

test('afficher le nom complet de l\'utilisateur', () => {
    render(<ProfilePage/>);
    const userNameElement = screen.getByText(/Sebastien Lacroix/i);
    expect(userNameElement).toBeInTheDocument();
});

test('afficher l\'email et le rôle de l\'utilisateur', () => {
    render(<ProfilePage/>);
    const emailElement = screen.getByText(/seb.lacroix@test.com/i);
    const roleElement = screen.getByText(/sre/i);
    expect(emailElement).toBeInTheDocument();
    expect(roleElement).toBeInTheDocument();
});

test('afficher la liste des incidents assignés', () => {
    render(<ProfilePage/>);
    const incidentTitle = screen.getByText(/Serveur de connexion inaccessible/i);
    expect(incidentTitle).toBeInTheDocument();
});
