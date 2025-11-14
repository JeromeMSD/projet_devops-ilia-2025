import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import { Dashboard } from './Dashboard';

const authUserMock = vi.fn();

vi.mock('react-auth-kit/hooks/useAuthUser', () => ({
    default: () => authUserMock(),
}));

describe('Dashboard', () => {
    it('renders a friendly fallback when no user is available', () => {
        authUserMock.mockReturnValue(null);

        render(<Dashboard/>);

        expect(
            screen.getByText('Impossible de récupérer vos informations utilisateur.'),
        ).toBeInTheDocument();
    });
});
