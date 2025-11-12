import type { ReactNode } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { act, renderHook } from '@testing-library/react';
import { describe, expect, it, vi, afterEach } from 'vitest';

const signInSpy = vi.fn(() => true);

vi.mock('react-auth-kit/hooks/useSignIn', () => ({
    default: () => signInSpy,
}));

const createQueryClient = () =>
    new QueryClient({
        defaultOptions: {
            queries: { retry: false },
            mutations: { retry: false },
        },
    });

const loadUseLogin = async () => {
    vi.resetModules();
    vi.stubEnv('VITE_API_URL', 'http://auth.local');

    return import('./useLogin');
};

afterEach(() => {
    vi.unstubAllEnvs();
    vi.clearAllMocks();
});

describe('useLogin', () => {
    it('performs a successful API login and caches the user', async () => {
        const loginResponse = {
            message: 'ok',
            user: {
                id_user: '1',
                firstname: 'John',
                lastname: 'Doe',
                email: 'john@example.com',
                role: 'USER' as const,
                created_at: new Date().toISOString(),
                token: 'jwt-token',
            },
        };

        global.fetch = vi.fn().mockResolvedValue({
            ok: true,
            json: async () => loginResponse,
        } as Response);

        const { useLogin } = await loadUseLogin();
        const queryClient = createQueryClient();
        const wrapper = ({ children }: { children: ReactNode }) => (
            <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
        );

        const { result } = renderHook(() => useLogin(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ email: 'john@example.com', password: 'secret' });
        });

        expect(global.fetch).toHaveBeenCalledWith(
            'http://auth.local/api/v1/login',
            expect.objectContaining({
                method: 'POST',
                body: JSON.stringify({ email: 'john@example.com', password: 'secret' }),
            }),
        );
        expect(signInSpy).toHaveBeenCalledWith({
            auth: { token: 'jwt-token', type: 'Bearer' },
            userState: loginResponse.user,
        });
        expect(queryClient.getQueryData(['currentUser'])).toEqual(loginResponse.user);
    });

    it('throws when the API response does not contain a token', async () => {
        const loginResponse = {
            message: 'ok',
            user: {
                id_user: '1',
                firstname: 'John',
                lastname: 'Doe',
                email: 'john@example.com',
                role: 'USER' as const,
                created_at: new Date().toISOString(),
            },
        };

        global.fetch = vi.fn().mockResolvedValue({
            ok: true,
            json: async () => loginResponse,
        } as Response);

        const { useLogin } = await loadUseLogin();
        const queryClient = createQueryClient();
        const wrapper = ({ children }: { children: ReactNode }) => (
            <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
        );

        const { result } = renderHook(() => useLogin(), { wrapper });

        await expect(
            act(async () => {
                await result.current.mutateAsync({ email: 'john@example.com', password: 'secret' });
            }),
        ).rejects.toThrow('Token manquant dans la réponse du serveur');
    });

    it('throws a network error when the server is unreachable', async () => {
        global.fetch = vi.fn().mockRejectedValue(new Error('network down'));

        const { useLogin } = await loadUseLogin();
        const queryClient = createQueryClient();
        const wrapper = ({ children }: { children: ReactNode }) => (
            <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
        );
        const { result } = renderHook(() => useLogin(), { wrapper });

        await expect(
            act(async () => {
                await result.current.mutateAsync({ email: 'a@example.com', password: 'b' });
            }),
        ).rejects.toThrow('Impossible de joindre le serveur');
    });
});
