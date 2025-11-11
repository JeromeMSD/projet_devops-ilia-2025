import type { ComponentProps } from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, beforeEach, vi } from 'vitest';

const navigateMock = vi.fn();

vi.mock('react-router', async () => {
    const actual = await vi.importActual<typeof import('react-router')>('react-router');
    return {
        ...actual,
        useNavigate: () => navigateMock,
    };
});

type UseLoginReturn = {
    mutate: ReturnType<typeof vi.fn>;
    mutateAsync: ReturnType<typeof vi.fn>;
    reset: ReturnType<typeof vi.fn>;
    error: Error | null;
    isPending: boolean;
};

const loginHookMocks = vi.hoisted(() => ({
    useLogin: vi.fn(),
}));

vi.mock('@/auth/useLogin', () => ({
    useLogin: loginHookMocks.useLogin,
}));

import { LoginForm } from './LoginForm';

const renderForm = (props: ComponentProps<typeof LoginForm> = {}) => render(<LoginForm {...props}/>);

describe('LoginForm', () => {
    let mutateMock: ReturnType<typeof vi.fn>;
    let resetMock: ReturnType<typeof vi.fn>;
    let hookState: UseLoginReturn;

    beforeEach(() => {
        mutateMock = vi.fn();
        resetMock = vi.fn();
        navigateMock.mockReset();
        hookState = {
            mutate: mutateMock,
            mutateAsync: mutateMock,
            reset: resetMock,
            error: null,
            isPending: false,
        };
        loginHookMocks.useLogin.mockReturnValue(hookState);
    });

    it('displays validation errors when fields are empty', async () => {
        renderForm();
        const user = userEvent.setup();

        await user.click(screen.getByRole('button', { name: /se connecter/i }));

        expect(await screen.findByText('Adresse email requise')).toBeInTheDocument();
        expect(await screen.findByText('Mot de passe requis')).toBeInTheDocument();
    });

    it('submits credentials and navigates to the dashboard on success', async () => {
        renderForm();
        const user = userEvent.setup();

        await user.type(screen.getByLabelText('Adresse email'), 'john@example.com');
        await user.type(screen.getByLabelText('Mot de passe'), 'secret');
        await user.click(screen.getByRole('button', { name: /se connecter/i }));

        expect(resetMock).toHaveBeenCalledTimes(1);
        expect(mutateMock).toHaveBeenCalledTimes(1);
        expect(mutateMock).toHaveBeenCalledWith(
            { email: 'john@example.com', password: 'secret' },
            expect.objectContaining({
                onSuccess: expect.any(Function),
            }),
        );

        const [, options] = mutateMock.mock.calls[0];
        await options.onSuccess();

        expect(navigateMock).toHaveBeenCalledWith('/dashboard');
    });

    it('renders server-side errors returned by the login hook', () => {
        hookState.error = new Error('Invalid credentials');
        loginHookMocks.useLogin.mockReturnValue(hookState);

        renderForm();

        expect(screen.getByText('Invalid credentials')).toBeInTheDocument();
    });
});
