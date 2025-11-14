import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import IncidentCreatePage from './IncidentCreatePage';
import { BrowserRouter } from 'react-router';
import { expect, test, vi } from 'vitest';

const renderPage = () => {
    render(
        <BrowserRouter>
            <IncidentCreatePage />
        </BrowserRouter>,
    );

    return {
        user: userEvent.setup(),
    };
};

test('doit afficher les champs du formulaire de création', () => {
    renderPage();
    const titleInput = screen.getByLabelText(/Titre de l'incident/i);
    const severitySelect = screen.getByLabelText(/Sévérité/i);
    const submitButton = screen.getByRole('button', { name: /Signaler l'incident/i });
    expect(titleInput).toBeInTheDocument();
    expect(severitySelect).toBeInTheDocument();
    expect(submitButton).toBeInTheDocument();
});

test('doit appeler l\'API POST /api/incidents lors de la soumission', async () => {
    const fetchSpy = vi.spyOn(window, 'fetch');
    const { user } = renderPage();
    const titleInput = screen.getByLabelText(/Titre de l'incident/i);
    const severitySelect = screen.getByLabelText(/Sévérité/i);
    const submitButton = screen.getByRole('button', { name: /Signaler l'incident/i });
    await user.type(titleInput, 'Panne majeure du serveur de login');
    await user.selectOptions(severitySelect, '1');
    await user.click(submitButton);
    expect(fetchSpy).toHaveBeenCalledTimes(1);
    expect(fetchSpy).toHaveBeenCalledWith(
        'http://localhost:8081/api/incidents',
        expect.objectContaining({
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: 'Panne majeure du serveur de login',
                sev: 1,
            }),
        }),
    );
});
