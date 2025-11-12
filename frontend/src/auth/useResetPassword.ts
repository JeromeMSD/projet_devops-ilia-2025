import { useMutation } from '@tanstack/react-query';

type ResetPasswordPayload = {
    reset_token: string;
    new_password: string;
};

type ResetPasswordResponse = {
    message?: string;
};

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:5010';

export function useResetPassword() {
    return useMutation({
        mutationFn: async (payload: ResetPasswordPayload) => {
            let response: Response;
            try {
                response = await fetch(`${API_BASE_URL}/api/v1/reset-password`, {
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
                throw new Error(message ?? 'Impossible de réinitialiser le mot de passe');
            }

            return body as ResetPasswordResponse;
        },
    });
}
