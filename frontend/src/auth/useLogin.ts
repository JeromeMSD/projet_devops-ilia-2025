import { useMutation, useQueryClient } from '@tanstack/react-query';
import useSignIn from 'react-auth-kit/hooks/useSignIn';
import type { LoginResponse } from '@/auth/types';

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:5001';

export function useLogin() {
    const signIn = useSignIn();
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (payload: { username: string; password: string }) => {
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
