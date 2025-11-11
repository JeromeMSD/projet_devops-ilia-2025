import { MemoryRouter, Route, Routes } from 'react-router';
import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import { ProtectedRoute } from './ProtectedRoute';

const useIsAuthenticatedMock = vi.fn();

vi.mock('react-auth-kit/hooks/useIsAuthenticated', () => ({
    default: () => useIsAuthenticatedMock(),
}));

const renderWithRouter = () =>
    render(
        <MemoryRouter initialEntries={['/dashboard']}>
            <Routes>
                <Route
                    path="/dashboard"
                    element={(
                        <ProtectedRoute>
                            <div>Dashboard Content</div>
                        </ProtectedRoute>
                    )}
                />
                <Route path="/login" element={<div>Login Page</div>}/>
            </Routes>
        </MemoryRouter>,
    );

describe('ProtectedRoute', () => {
    it('renders children when the user is authenticated', () => {
        useIsAuthenticatedMock.mockReturnValue(true);

        renderWithRouter();

        expect(screen.getByText('Dashboard Content')).toBeInTheDocument();
    });

    it('redirects to /login when the user is not authenticated', () => {
        useIsAuthenticatedMock.mockReturnValue(false);

        renderWithRouter();

        expect(screen.getByText('Login Page')).toBeInTheDocument();
    });
});
