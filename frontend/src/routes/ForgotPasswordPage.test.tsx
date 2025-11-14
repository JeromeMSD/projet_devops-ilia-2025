import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';

import { ForgotPasswordPage } from './ForgotPasswordPage';

vi.mock('@/components/ForgotPasswordForm', () => ({
    ForgotPasswordForm: () => <div data-testid="forgot-password-form">Mocked form</div>,
}));

describe('ForgotPasswordPage', () => {
    it('renders the forgot password form', () => {
        render(<ForgotPasswordPage />);

        expect(screen.getByTestId('forgot-password-form')).toBeInTheDocument();
    });
});
