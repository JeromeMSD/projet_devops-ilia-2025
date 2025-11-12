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

const loadUseRegister = async () => {
    vi.resetModules();
    vi.stubEnv('VITE_API_URL', 'http://auth.local');

    return import('./useRegister');
};

afterEach(() => {
    vi.unstubAllEnvs();
    vi.clearAllMocks();
});

describe('useRegister', () => {
    it('posts registration payload and returns the response body', async () => {
        const registerResponse = {
            message: 'Utilisateur créé avec succès',
            user: {
                id_user: '1',
                firstname: 'Jane',
                lastname: 'Doe',
                email: 'jane@example.com',
                role: 'USER' as const,
                created_at: new Date().toISOString(),
            },
        };

        global.fetch = vi.fn().mockResolvedValue({
            ok: true,
            json: async () => registerResponse,
        } as Response);

        const { useRegister } = await loadUseRegister();
        const queryClient = createQueryClient();
        const wrapper = ({ children }: { children: ReactNode }) => (
            <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
        );

        const { result } = renderHook(() => useRegister(), { wrapper });

        await act(async () => {
            const data = await result.current.mutateAsync({
                firstname: 'Jane',
                lastname: 'Doe',
                email: 'jane@example.com',
                password: 'Password123',
                role: 'USER',
            });

            expect(data).toEqual(registerResponse);
        });

        expect(global.fetch).toHaveBeenCalledWith(
            'http://auth.local/api/v1/register',
            expect.objectContaining({
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    firstname: 'Jane',
                    lastname: 'Doe',
                    email: 'jane@example.com',
                    password: 'Password123',
                    role: 'USER',
                }),
            }),
        );
    });

    it('throws friendly error messages when API fails', async () => {
        global.fetch = vi.fn().mockResolvedValue({
            ok: false,
            json: async () => ({ error: 'Conflit' }),
        } as Response);

        const { useRegister } = await loadUseRegister();
        const queryClient = createQueryClient();
        const wrapper = ({ children }: { children: ReactNode }) => (
            <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
        );

        const { result } = renderHook(() => useRegister(), { wrapper });

        await expect(
            act(async () => {
                await result.current.mutateAsync({
                    firstname: 'Jane',
                    lastname: 'Doe',
                    email: 'jane@example.com',
                    password: 'Password123',
                    role: 'USER',
                });
            }),
        ).rejects.toThrow('Conflit');
    });

    it('throws network error when fetch fails', async () => {
        global.fetch = vi.fn().mockRejectedValue(new Error('network down'));

        const { useRegister } = await loadUseRegister();
        const queryClient = createQueryClient();
        const wrapper = ({ children }: { children: ReactNode }) => (
            <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
        );

        const { result } = renderHook(() => useRegister(), { wrapper });

        await expect(
            act(async () => {
                await result.current.mutateAsync({
                    firstname: 'Jane',
                    lastname: 'Doe',
                    email: 'jane@example.com',
                    password: 'Password123',
                    role: 'USER',
                });
            }),
        ).rejects.toThrow('Impossible de joindre le serveur');
    });
});
