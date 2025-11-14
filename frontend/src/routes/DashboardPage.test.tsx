import { render, screen, within } from '@testing-library/react';
import DashboardPage from './DashboardPage';
import { vi } from 'vitest';

vi.mock('react-auth-kit/hooks/useAuthUser', () => ({
    default: () => ({
        id_user: 'user-123-abc',
        firstname: 'Oumnia',
        lastname: 'SRE',
        email: 'oumnia@sre.com',
        role: 'SRE',
        created_at: '2024-01-01T00:00:00.000Z',
    }),
}));

vi.mock('../mocks/mockData', () => ({
    mockUser: {
        user_id: 'user-123-abc',
        username: 'Oumnia SRE',
        email: 'oumnia@sre.com',
        role: 'sre',
    },
    mockIncidents: [
        { id: 'inc-001', title: 'Serveur critique', severity: 'critique', assignee_id: 'user-123-abc' },
        { id: 'inc-003', title: 'Fichier critique', severity: 'critique', assignee_id: 'user-456-xyz' },
        { id: 'inc-002', title: 'Bug majeur', severity: 'majeure', assignee_id: 'user-123-abc' },
        { id: 'inc-004', title: 'Problème mineur', severity: 'mineure' },
    ],
}));
test('doit afficher le résumé des incidents critiques (2)', () => {
    render(<DashboardPage />);
    const summaryLabel = screen.getByText(/Incidents Critiques en Cours/i);
    const summaryContainer = summaryLabel.closest('div');
    expect(summaryContainer).not.toBeNull();
    const summaryCount = within(summaryContainer!).getByText('2');
    expect(summaryCount).toBeInTheDocument();
});
test('doit afficher uniquement les incidents assignés à l\'utilisateur (2)', () => {
    render(<DashboardPage />);
    const assignedIncident1 = screen.getByText(/Serveur critique/i);
    const assignedIncident2 = screen.getByText(/Bug majeur/i);
    const unassignedIncident = screen.queryByText(/Fichier critique/i);
    expect(assignedIncident1).toBeInTheDocument();
    expect(assignedIncident2).toBeInTheDocument();
    expect(unassignedIncident).not.toBeInTheDocument();
});
