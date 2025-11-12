import { useMutation, useQueryClient } from '@tanstack/react-query';
import useSignIn from 'react-auth-kit/hooks/useSignIn';

import type { LoginResponse } from '@/auth/types';

const API_BASE_URL = import.meta.env.VITE_USER_API_URL ?? 'http://localhost:5010';

export function useLogin() {
    const signIn = useSignIn();
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (payload: { email: string; password: string }) => {
            let response: Response;
            try {
                response = await fetch(`${API_BASE_URL}/api/v1/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });
            } catch {
                throw new Error('Impossible de joindre le serveur');
            }

            const body = await response.json().catch(() => null);

            if (!response.ok) {
                const message = typeof body === 'object' && body !== null
                    ? 'error' in body
                        ? String(body.error)
                        : 'message' in body
                            ? String(body.message)
                            : null
                    : null;
                throw new Error(message ?? 'Identifiants invalides');
            }

            return body as LoginResponse;
        },
        onSuccess: (data) => {
            const token = data?.user.token ?? null;
            if (!token) {
                throw new Error('Token manquant dans la réponse du serveur');
            }

            const ok = signIn({
                auth: {
                    token,
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
