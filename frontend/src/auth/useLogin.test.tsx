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

const loadUseLogin = async (mode: 'api' | 'mock' = 'api') => {
    vi.resetModules();
    vi.stubEnv('VITE_AUTH_MODE', mode);
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
            token: 'jwt-token',
            user: {
                user_id: '1',
                username: 'john',
                email: 'john@example.com',
                role: 'user' as const,
                created_at: new Date().toISOString(),
            },
        };

        global.fetch = vi.fn().mockResolvedValue({
            ok: true,
            json: async () => loginResponse,
        } as Response);

        const { useLogin } = await loadUseLogin('api');
        const queryClient = createQueryClient();
        const wrapper = ({ children }: { children: ReactNode }) => (
            <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
        );

        const { result } = renderHook(() => useLogin(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ username: 'john', password: 'secret' });
        });

        expect(global.fetch).toHaveBeenCalledWith(
            'http://auth.local/api/v1/auth/login',
            expect.objectContaining({
                method: 'POST',
            }),
        );
        expect(signInSpy).toHaveBeenCalledWith({
            auth: { token: loginResponse.token, type: 'Bearer' },
            userState: loginResponse.user,
        });
        expect(queryClient.getQueryData(['currentUser'])).toEqual(loginResponse.user);
    });

    it('throws a network error when the server is unreachable', async () => {
        global.fetch = vi.fn().mockRejectedValue(new Error('network down'));

        const { useLogin } = await loadUseLogin('api');
        const queryClient = createQueryClient();
        const wrapper = ({ children }: { children: ReactNode }) => (
            <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
        );
        const { result } = renderHook(() => useLogin(), { wrapper });

        await expect(
            act(async () => {
                await result.current.mutateAsync({ username: 'a', password: 'b' });
            }),
        ).rejects.toThrow('Impossible de joindre le serveur');
    });

    it('returns a mocked response when mock mode is enabled', async () => {
        global.fetch = vi.fn();

        const { useLogin } = await loadUseLogin('mock');
        const queryClient = createQueryClient();
        const wrapper = ({ children }: { children: ReactNode }) => (
            <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
        );
        const { result } = renderHook(() => useLogin(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ username: 'demo', password: 'secret' });
        });

        expect(global.fetch).not.toHaveBeenCalled();
        expect(signInSpy).toHaveBeenCalledTimes(1);
        expect(queryClient.getQueryData(['currentUser'])).toMatchObject({
            username: 'demo',
            role: 'user',
        });
    });
});
