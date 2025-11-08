import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router';
import App from './App';

describe('App', () => {
    const renderWithRouter = () =>
        render(
            <BrowserRouter>
                <App/>
            </BrowserRouter>,
        );

    it('shows the hero content and navigation links', () => {
        renderWithRouter();

        expect(screen.getByRole('heading', { level: 1, name: /friendly react \+ vite baseline/i })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: /home/i })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: /about/i })).toBeInTheDocument();
    });
});
