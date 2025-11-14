import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';

import { ResetPasswordPage } from './ResetPasswordPage';

vi.mock('@/components/ResetPasswordForm', () => ({
    ResetPasswordForm: () => <div data-testid="reset-password-form">Mock form</div>,
}));

describe('ResetPasswordPage', () => {
    it('renders the reset password form wrapper', () => {
        render(<ResetPasswordPage />);

        expect(screen.getByTestId('reset-password-form')).toBeInTheDocument();
    });
});
