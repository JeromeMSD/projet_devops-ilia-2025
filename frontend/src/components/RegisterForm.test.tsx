import { type ComponentProps } from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';

const navigateMock = vi.fn();

vi.mock('react-router', async () => {
    const actual = await vi.importActual<typeof import('react-router')>('react-router');
    return {
        ...actual,
        useNavigate: () => navigateMock,
        Link: ({ to, children }: { to: string; children: React.ReactNode }) => (
            <a href={String(to)}>{children}</a>
        ),
    };
});

type RegisterHookState = {
    mutate: ReturnType<typeof vi.fn>;
    mutateAsync: ReturnType<typeof vi.fn>;
    reset: ReturnType<typeof vi.fn>;
    error: Error | null;
    isPending: boolean;
};

const registerHookMocks = vi.hoisted(() => ({
    useRegister: vi.fn(),
}));

vi.mock('@/auth/useRegister', () => ({
    useRegister: registerHookMocks.useRegister,
}));

const loginHookMocks = vi.hoisted(() => ({
    useLogin: vi.fn(),
}));

vi.mock('@/auth/useLogin', () => ({
    useLogin: loginHookMocks.useLogin,
}));

import { RegisterForm } from './RegisterForm';
import * as React from 'react';

const renderForm = (props: ComponentProps<typeof RegisterForm> = {}) => render(<RegisterForm {...props}/>);

describe('RegisterForm', () => {
    let registerMutateAsyncMock: ReturnType<typeof vi.fn>;
    let registerResetMock: ReturnType<typeof vi.fn>;
    let registerState: RegisterHookState;
    let loginMutateAsyncMock: ReturnType<typeof vi.fn>;
    let loginResetMock: ReturnType<typeof vi.fn>;
    let loginState: RegisterHookState;

    beforeEach(() => {
        registerMutateAsyncMock = vi.fn().mockResolvedValue({ message: 'ok' });
        registerResetMock = vi.fn();
        loginMutateAsyncMock = vi.fn().mockResolvedValue(undefined);
        loginResetMock = vi.fn();
        navigateMock.mockReset();

        registerState = {
            mutate: vi.fn(),
            mutateAsync: registerMutateAsyncMock,
            reset: registerResetMock,
            error: null,
            isPending: false,
        };
        loginState = {
            mutate: vi.fn(),
            mutateAsync: loginMutateAsyncMock,
            reset: loginResetMock,
            error: null,
            isPending: false,
        };
        registerHookMocks.useRegister.mockReturnValue(registerState);
        loginHookMocks.useLogin.mockReturnValue(loginState);
    });

    it('displays validation errors when fields are empty', async () => {
        renderForm();
        const user = userEvent.setup();

        await user.click(screen.getByRole('button', { name: /créer le compte/i }));

        expect(await screen.findByText('Prénom requis')).toBeInTheDocument();
        expect(await screen.findByText('Nom requis')).toBeInTheDocument();
        expect(await screen.findByText('Adresse email requise')).toBeInTheDocument();
        expect(await screen.findByText('Le mot de passe doit contenir au moins 6 caractères, une majuscule et un chiffre')).toBeInTheDocument();
    });

    it('submits values and shows success message', async () => {
        renderForm();
        const user = userEvent.setup();

        await user.type(screen.getByLabelText('Prénom'), 'Jane');
        await user.type(screen.getByLabelText('Nom'), 'Doe');
        await user.type(screen.getByLabelText('Adresse email'), 'jane@example.com');
        await user.type(screen.getByLabelText('Mot de passe'), 'Password123');
        await user.selectOptions(screen.getByLabelText('Rôle'), 'SRE');
        await user.click(screen.getByRole('button', { name: /créer le compte/i }));

        expect(registerResetMock).toHaveBeenCalledTimes(1);
        await waitFor(() => {
            expect(registerMutateAsyncMock).toHaveBeenCalledWith({
                firstname: 'Jane',
                lastname: 'Doe',
                email: 'jane@example.com',
                password: 'Password123',
                role: 'SRE',
            });
        });

        await waitFor(() => {
            expect(loginMutateAsyncMock).toHaveBeenCalledWith({
                email: 'jane@example.com',
                password: 'Password123',
            });
        });

        expect(await screen.findByText('ok')).toBeInTheDocument();
        expect(navigateMock).toHaveBeenCalledWith('/dashboard');
    });

    it('renders API errors returned by the register hook', () => {
        registerState.error = new Error('Conflit');
        registerHookMocks.useRegister.mockReturnValue(registerState);

        renderForm();

        expect(screen.getByText('Conflit')).toBeInTheDocument();
    });
});
