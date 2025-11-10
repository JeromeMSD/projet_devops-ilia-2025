import React from 'react';
import { render, screen } from '@testing-library/react';
import DashboardPage from './DashboardPage'; 
import { vi } from 'vitest';
vi.mock('../mocks/mockData', () => ({
    mockUser: {
        username: "Oumnia SRE",
        email: "oumnia@sre.com",
        role: "sre"
    },
    mockIncidents: [
        { id: "inc-001", title: "Serveur critique", severity: "critique" },
        { id: "inc-003", title: "Fichier critique", severity: "critique" }, 
        { id: "inc-002", title: "Bug majeur", severity: "majeure" },
        { id: "inc-004", title: "Problème mineur", severity: "mineure" }
    ]
}));
test('doit afficher le résumé des incidents critiques (2)', () => {
    render(<DashboardPage />);
    const summaryElement = screen.getByText(/2 Incidents Critiques en cours/i);

    expect(summaryElement).toBeInTheDocument();
});