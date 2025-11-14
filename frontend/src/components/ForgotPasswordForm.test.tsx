import type { ComponentProps } from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';

type MutationHookState = {
    mutate: ReturnType<typeof vi.fn>;
    mutateAsync: ReturnType<typeof vi.fn>;
    reset: ReturnType<typeof vi.fn>;
    error: Error | null;
    isPending: boolean;
    isSuccess: boolean;
    data: { message?: string; reset_token?: string } | null;
};

const forgotHookMocks = vi.hoisted(() => ({
    useForgotPassword: vi.fn(),
}));

vi.mock('@/auth/useForgotPassword', () => ({
    useForgotPassword: forgotHookMocks.useForgotPassword,
}));

import { ForgotPasswordForm } from './ForgotPasswordForm';

const renderForm = (props: ComponentProps<typeof ForgotPasswordForm> = {}) => render(<ForgotPasswordForm {...props}/>);

describe('ForgotPasswordForm', () => {
    let mutateMock: ReturnType<typeof vi.fn>;
    let hookState: MutationHookState;

    beforeEach(() => {
        mutateMock = vi.fn((_payload, options?: { onSuccess?: (data: unknown) => void }) => {
            options?.onSuccess?.({ message: 'ok' });
        });
        hookState = {
            mutate: mutateMock,
            mutateAsync: mutateMock,
            reset: vi.fn(),
            error: null,
            isPending: false,
            isSuccess: true,
            data: { message: 'ok' },
        };
        forgotHookMocks.useForgotPassword.mockReturnValue(hookState);
    });

    it('shows validation errors for empty email', async () => {
        renderForm();
        const user = userEvent.setup();

        await user.click(screen.getByRole('button', { name: /envoyer le lien/i }));

        expect(await screen.findByText('Adresse email requise')).toBeInTheDocument();
    });

    it('submits email and displays success message', async () => {
        renderForm();
        const user = userEvent.setup();

        await user.type(screen.getByLabelText('Adresse email'), 'user@example.com');
        await user.click(screen.getByRole('button', { name: /envoyer le lien/i }));

        expect(hookState.reset).toHaveBeenCalledTimes(1);
        expect(mutateMock).toHaveBeenCalledWith(
            { email: 'user@example.com' },
            expect.objectContaining({
                onSuccess: expect.any(Function),
            }),
        );
        expect(await screen.findByText('ok')).toBeInTheDocument();
    });

    it('renders server errors', () => {
        hookState.error = new Error('Erreur');
        hookState.data = null;
        forgotHookMocks.useForgotPassword.mockReturnValue(hookState);

        renderForm();

        expect(screen.getByText('Erreur')).toBeInTheDocument();
    });
});
