import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';

import { RegisterPage } from './RegisterPage';

vi.mock('@/components/RegisterForm', () => ({
    RegisterForm: () => <div data-testid="register-form">Mock form</div>,
}));

describe('RegisterPage', () => {
    it('renders the register form block', () => {
        render(<RegisterPage />);

        expect(screen.getByTestId('register-form')).toBeInTheDocument();
    });
});
