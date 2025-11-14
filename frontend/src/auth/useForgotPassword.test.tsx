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

const loadUseForgotPassword = async () => {
    vi.resetModules();
    vi.stubEnv('VITE_USER_API_URL', 'http://auth.local');

    return import('./useForgotPassword');
};

afterEach(() => {
    vi.unstubAllEnvs();
    vi.clearAllMocks();
});

describe('useForgotPassword', () => {
    it('posts email to forgot-password endpoint', async () => {
        const responseBody = { message: 'Si cet email existe...' };

        global.fetch = vi.fn().mockResolvedValue({
            ok: true,
            json: async () => responseBody,
        } as Response);

        const { useForgotPassword } = await loadUseForgotPassword();
        const queryClient = createQueryClient();
        const wrapper = ({ children }: { children: ReactNode }) => (
            <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
        );

        const { result } = renderHook(() => useForgotPassword(), { wrapper });

        await act(async () => {
            const data = await result.current.mutateAsync({ email: 'user@example.com' });
            expect(data).toEqual(responseBody);
        });

        expect(global.fetch).toHaveBeenCalledWith(
            'http://auth.local/api/v1/forgot-password',
            expect.objectContaining({
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: 'user@example.com' }),
            }),
        );
    });

    it('throws when the server returns an error', async () => {
        global.fetch = vi.fn().mockResolvedValue({
            ok: false,
            json: async () => ({ error: 'Format d\'email invalide' }),
        } as Response);

        const { useForgotPassword } = await loadUseForgotPassword();
        const queryClient = createQueryClient();
        const wrapper = ({ children }: { children: ReactNode }) => (
            <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
        );

        const { result } = renderHook(() => useForgotPassword(), { wrapper });

        await expect(
            act(async () => {
                await result.current.mutateAsync({ email: 'bad' });
            }),
        ).rejects.toThrow('Format d\'email invalide');
    });
});
