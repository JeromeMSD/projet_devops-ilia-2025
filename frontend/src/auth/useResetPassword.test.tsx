import type { ReactNode } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { act, renderHook } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

const createQueryClient = () =>
    new QueryClient({
        defaultOptions: {
            queries: { retry: false },
            mutations: { retry: false },
        },
    });

const loadUseResetPassword = async () => {
    vi.resetModules();
    vi.stubEnv('VITE_USER_API_URL', 'http://auth.local');

    return import('./useResetPassword');
};

afterEach(() => {
    vi.unstubAllEnvs();
    vi.clearAllMocks();
});

describe('useResetPassword', () => {
    it('sends the reset token and new password to the API', async () => {
        const responseBody = { message: 'Mot de passe réinitialisé avec succès' };
        global.fetch = vi.fn().mockResolvedValue({
            ok: true,
            json: async () => responseBody,
        } as Response);

        const { useResetPassword } = await loadUseResetPassword();
        const queryClient = createQueryClient();
        const wrapper = ({ children }: { children: ReactNode }) => (
            <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
        );

        const { result } = renderHook(() => useResetPassword(), { wrapper });

        await act(async () => {
            const data = await result.current.mutateAsync({
                reset_token: 'token',
                new_password: 'Password1',
            });
            expect(data).toEqual(responseBody);
        });

        expect(global.fetch).toHaveBeenCalledWith(
            'http://auth.local/api/v1/reset-password',
            expect.objectContaining({
                method: 'POST',
                body: JSON.stringify({
                    reset_token: 'token',
                    new_password: 'Password1',
                }),
            }),
        );
    });

    it('surfaces API errors', async () => {
        global.fetch = vi.fn().mockResolvedValue({
            ok: false,
            json: async () => ({ error: 'Token invalide' }),
        } as Response);

        const { useResetPassword } = await loadUseResetPassword();
        const queryClient = createQueryClient();
        const wrapper = ({ children }: { children: ReactNode }) => (
            <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
        );

        const { result } = renderHook(() => useResetPassword(), { wrapper });

        await expect(
            act(async () => {
                await result.current.mutateAsync({
                    reset_token: 'bad',
                    new_password: 'Password1',
                });
            }),
        ).rejects.toThrow('Token invalide');
    });
});
