import { render, screen } from '@testing-library/react';
import IncidentCreatePage from '/Users/air/FrontendDevops/projet_devops-ilia-2025/frontend/src/routes/IncidentCreatePage.tsx';
// On doit simuler le routeur car la page utilisera la navigation
import { BrowserRouter } from 'react-router-dom';
import { expect, test } from 'vitest';

const renderPage = () => {
    render(
        <BrowserRouter>
        <IncidentCreatePage />
        </BrowserRouter>
    );
};

test('doit afficher les champs du formulaire de création', () => {
    renderPage();
    const titleInput = screen.getByLabelText(/Titre de l'incident/i);
    const submitButton = screen.getByRole('button', { name: /Signaler l'incident/i });
    expect(titleInput).toBeInTheDocument();
    expect(submitButton).toBeInTheDocument();
});