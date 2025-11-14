import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';

import { LoginPage } from './LoginPage';

vi.mock('@/components/LoginForm', () => ({
    LoginForm: () => <div data-testid="login-form">Mocked login form</div>,
}));

describe('LoginPage', () => {
    it('renders the login form container', () => {
        render(<LoginPage />);

        expect(screen.getByTestId('login-form')).toBeInTheDocument();
    });
});
