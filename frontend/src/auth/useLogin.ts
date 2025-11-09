import { useMutation, useQueryClient } from '@tanstack/react-query';
import useSignIn from 'react-auth-kit/hooks/useSignIn';
import type { LoginResponse } from '@/auth/types';

const API_BASE_URL = 'http://localhost:5001';

export function useLogin() {
    const signIn = useSignIn();
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (payload: { username: string; password: string }) => {
            const res = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            if (!res.ok) {
                throw new Error('Invalid credentials');
            }

            return (await res.json()) as LoginResponse;
        },
        onSuccess: async (data) => {
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

            await queryClient.invalidateQueries({ queryKey: ['currentUser'] });
        },
    });
}
