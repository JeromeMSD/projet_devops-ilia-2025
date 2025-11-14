import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router';

vi.mock('react-auth-kit/hooks/useIsAuthenticated', () => ({
    default: () => false,
}));

vi.mock('react-auth-kit/hooks/useSignOut', () => ({
    default: () => vi.fn(),
}));

vi.mock('react-auth-kit/hooks/useAuthUser', () => ({
    default: () => null,
}));

const logoutHookMock = {
    mutate: vi.fn(),
    mutateAsync: vi.fn(),
    reset: vi.fn(),
    error: null,
    isPending: false,
};

vi.mock('@/auth/useLogout', () => ({
    useLogout: () => logoutHookMock,
}));

import App from './App';

describe('App', () => {
    const renderWithRouter = () =>
        render(
            <BrowserRouter>
                <App />
            </BrowserRouter>,
        );

    it('shows the navigation links', () => {
        renderWithRouter();

        expect(screen.getByRole('link', { name: /home/i })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: /about/i })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: /incidents/i })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: /login/i })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: /register/i })).toBeInTheDocument();
    });
});
