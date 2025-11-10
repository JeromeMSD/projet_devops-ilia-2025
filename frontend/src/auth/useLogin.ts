import { useMutation, useQueryClient } from '@tanstack/react-query';
import useSignIn from 'react-auth-kit/hooks/useSignIn';

import type { LoginResponse } from '@/auth/types';

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:5001';
const IS_MOCK_MODE = (import.meta.env.VITE_AUTH_MODE ?? 'api').toLowerCase() === 'mock';

async function mockLogin(payload: { username: string; password: string }): Promise<LoginResponse> {
    // TODO: Delete when the user service is ready
    const toBase64Url = (value: Record<string, unknown>) => {
        const json = JSON.stringify(value);

        if (typeof globalThis.btoa === 'function') {
            return globalThis.btoa(json)
                .replace(/\+/g, '-')
                .replace(/\//g, '_')
                .replace(/=+$/, '');
        }

        const bufferCtor = (globalThis as {
            Buffer?: { from(input: string, encoding: string): { toString(encoding: string): string } }
        }).Buffer;
        if (bufferCtor) {
            return bufferCtor.from(json, 'utf-8')
                .toString('base64')
                .replace(/\+/g, '-')
                .replace(/\//g, '_')
                .replace(/=+$/, '');
        }

        throw new Error('Base64 encoding not supported in this environment');
    };

    const createMockJwt = (username: string) => {
        const header = { alg: 'HS256', typ: 'JWT' };
        const exp = Math.floor(Date.now() / 1000) + 60 * 60; // 1 hour lifetime
        const payload = {
            sub: username,
            exp,
            iat: Math.floor(Date.now() / 1000),
        };

        return `${toBase64Url(header)}.${toBase64Url(payload)}.mock-signature`;
    };

    await new Promise((resolve) => setTimeout(resolve, 600));

    const username = payload.username.trim() || 'demo';

    return {
        message: 'Connexion simulée (service d\'auth indisponible)',
        token: createMockJwt(username),
        user: {
            user_id: `mock-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`,
            username,
            email: `${username}@example.com`,
            role: 'user',
            created_at: new Date().toISOString(),
        },
    };
}

export function useLogin() {
    const signIn = useSignIn();
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (payload: { username: string; password: string }) => {
            if (IS_MOCK_MODE) {
                return mockLogin(payload);
            }

            let response: Response;
            try {
                response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });
            } catch (error) {
                throw new Error('Impossible de joindre le serveur');
            }

            const body = await response.json().catch(() => null);

            if (!response.ok) {
                const message = typeof body === 'object' && body !== null && 'message' in body
                    ? String(body.message)
                    : 'Identifiants invalides';
                throw new Error(message);
            }

            return body as LoginResponse;
        },
        onSuccess: (data) => {
            const ok = signIn({
                auth: {
                    token: data.token,
                    type: 'Bearer',
                },
                userState: data.user,
            });

            if (!ok) {
                throw new Error('Sign-in failed');
            }

            queryClient.setQueryData(['currentUser'], data.user);
        },
    });
}
