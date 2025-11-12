import { useMutation } from '@tanstack/react-query';

import type { AuthUser } from '@/auth/types';

const API_BASE_URL = import.meta.env.VITE_USER_API_URL ?? 'http://localhost:5010';

type RegisterPayload = {
    firstname: string;
    lastname: string;
    email: string;
    password: string;
    role: AuthUser['role'];
};

type RegisterResponse = {
    message: string;
    user: AuthUser;
};

export function useRegister() {
    return useMutation({
        mutationFn: async (payload: RegisterPayload) => {
            let response: Response;
            try {
                response = await fetch(`${API_BASE_URL}/api/v1/register`, {
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
                throw new Error(message ?? 'Inscription impossible');
            }

            return body as RegisterResponse;
        },
    });
}
