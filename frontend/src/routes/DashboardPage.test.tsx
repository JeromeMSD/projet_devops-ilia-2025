import React from 'react';
import { render, screen } from '@testing-library/react';
import DashboardPage from './DashboardPage'; 
import { vi } from 'vitest';
vi.mock('../mocks/mockData', () => ({
    mockUser: {
        user_id: "user-123-abc", 
        username: "Oumnia SRE",
        email: "oumnia@sre.com",
        role: "sre"
    },
    mockIncidents: [
        { id: "inc-001", title: "Serveur critique", severity: "critique", assignee_id: "user-123-abc" }, 
        { id: "inc-003", title: "Fichier critique", severity: "critique", assignee_id: "user-456-xyz" }, 
        { id: "inc-002", title: "Bug majeur", severity: "majeure", assignee_id: "user-123-abc" }, 
        { id: "inc-004", title: "Problème mineur", severity: "mineure" } 
    ]
}));
test('doit afficher le résumé des incidents critiques (2)', () => {
    render(<DashboardPage />);
    const summaryElement = screen.getByText(/2 Incidents Critiques en cours/i);
    expect(summaryElement).toBeInTheDocument();
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