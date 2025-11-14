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
    data: { message?: string } | null;
};

const resetHookMocks = vi.hoisted(() => ({
    useResetPassword: vi.fn(),
}));

vi.mock('@/auth/useResetPassword', () => ({
    useResetPassword: resetHookMocks.useResetPassword,
}));

import { ResetPasswordForm } from './ResetPasswordForm';

const renderForm = (props: ComponentProps<typeof ResetPasswordForm> = {}) => render(<ResetPasswordForm {...props}/>);

describe('ResetPasswordForm', () => {
    let mutateMock: ReturnType<typeof vi.fn>;
    let hookState: MutationHookState;

    beforeEach(() => {
        mutateMock = vi.fn((_payload, options?: { onSuccess?: () => void }) => {
            options?.onSuccess?.();
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
        resetHookMocks.useResetPassword.mockReturnValue(hookState);
    });

    it('validates required fields', async () => {
        renderForm();
        const user = userEvent.setup();

        await user.click(screen.getByRole('button', { name: /réinitialiser/i }));

        expect(await screen.findByText('Token requis')).toBeInTheDocument();
        expect(
            await screen.findByText('Le mot de passe doit contenir au moins 6 caractères, une majuscule et un chiffre'),
        ).toBeInTheDocument();
    });

    it('submits token and new password', async () => {
        renderForm();
        const user = userEvent.setup();

        await user.type(screen.getByLabelText('Token de réinitialisation'), 'token');
        await user.type(screen.getByLabelText('Nouveau mot de passe'), 'Password1');
        await user.click(screen.getByRole('button', { name: /réinitialiser/i }));

        expect(hookState.reset).toHaveBeenCalledTimes(1);
        expect(mutateMock).toHaveBeenCalledWith(
            { reset_token: 'token', new_password: 'Password1' },
            expect.objectContaining({
                onSuccess: expect.any(Function),
            }),
        );
        expect(await screen.findByText('ok')).toBeInTheDocument();
    });

    it('renders API errors', () => {
        hookState.error = new Error('Token invalide');
        hookState.data = null;
        resetHookMocks.useResetPassword.mockReturnValue(hookState);

        renderForm();

        expect(screen.getByText('Token invalide')).toBeInTheDocument();
    });
});
