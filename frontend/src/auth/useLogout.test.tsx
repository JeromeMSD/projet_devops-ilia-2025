import type { ReactNode } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { act, renderHook, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

const signOutMock = vi.fn();
const authHeaderMock = vi.fn(() => 'Bearer token');

vi.mock('react-auth-kit/hooks/useSignOut', () => ({
    default: () => signOutMock,
}));

vi.mock('react-auth-kit/hooks/useAuthHeader', () => ({
    default: () => authHeaderMock(),
}));

const createQueryClient = () =>
    new QueryClient({
        defaultOptions: {
            queries: { retry: false },
            mutations: { retry: false },
        },
    });

const loadUseLogout = async () => {
    vi.resetModules();
    vi.stubEnv('VITE_API_URL', 'http://auth.local');

    return import('./useLogout');
};

afterEach(() => {
    vi.unstubAllEnvs();
    vi.clearAllMocks();
});

describe('useLogout', () => {
    it('calls the API, clears cache and signs out on success', async () => {
        const queryClient = createQueryClient();
        queryClient.setQueryData(['currentUser'], { id_user: '1' });

        const responseBody = { message: 'ok' };
        global.fetch = vi.fn().mockResolvedValue({
            ok: true,
            json: async () => responseBody,
        } as Response);

        const { useLogout } = await loadUseLogout();
        const wrapper = ({ children }: { children: ReactNode }) => (
            <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
        );

        const { result } = renderHook(() => useLogout(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync();
        });

        expect(global.fetch).toHaveBeenCalledWith(
            'http://auth.local/api/v1/logout',
            expect.objectContaining({
                method: 'POST',
                headers: expect.objectContaining({
                    Authorization: 'Bearer token',
                }),
            }),
        );
        await waitFor(() => {
            expect(signOutMock).toHaveBeenCalledTimes(1);
        });
        expect(queryClient.getQueryData(['currentUser'])).toBeUndefined();
    });

    it('propagates API errors with message body', async () => {
        global.fetch = vi.fn().mockResolvedValue({
            ok: false,
            json: async () => ({ error: 'Token révoqué' }),
        } as Response);

        const { useLogout } = await loadUseLogout();
        const queryClient = createQueryClient();
        const wrapper = ({ children }: { children: ReactNode }) => (
            <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
        );

        const { result } = renderHook(() => useLogout(), { wrapper });

        await expect(
            act(async () => {
                await result.current.mutateAsync();
            }),
        ).rejects.toThrow('Token révoqué');
        await waitFor(() => {
            expect(signOutMock).toHaveBeenCalledTimes(1);
        });
    });

    it('throws a network error when the request fails', async () => {
        global.fetch = vi.fn().mockRejectedValue(new Error('network down'));

        const { useLogout } = await loadUseLogout();
        const queryClient = createQueryClient();
        const wrapper = ({ children }: { children: ReactNode }) => (
            <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
        );

        const { result } = renderHook(() => useLogout(), { wrapper });

        await expect(
            act(async () => {
                await result.current.mutateAsync();
            }),
        ).rejects.toThrow('Impossible de joindre le serveur');
        await waitFor(() => {
            expect(signOutMock).toHaveBeenCalledTimes(1);
        });
    });
});
