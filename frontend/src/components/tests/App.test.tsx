import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from '../../App';

describe('App', () => {
    const renderWithRouter = () =>
        render(
            <BrowserRouter>
                <App />
            </BrowserRouter>,
        );

    it('shows the hero content and navigation links', () => {
        renderWithRouter();

        // Heading principal
        expect(screen.getByRole('heading', { level: 1, name: /polystatus/i })).toBeInTheDocument();

        // Liens de navigation
        expect(screen.getByRole('link', { name: /home/i })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: /about/i })).toBeInTheDocument();
    });
});
