import { useMutation } from '@tanstack/react-query';

type ForgotPasswordResponse = {
    message?: string;
    reset_token?: string;
};

const API_BASE_URL = import.meta.env.VITE_USER_API_URL ?? 'http://localhost:5010';

export function useForgotPassword() {
    return useMutation({
        mutationFn: async (payload: { email: string }) => {
            let response: Response;
            try {
                response = await fetch(`${API_BASE_URL}/api/v1/forgot-password`, {
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
                throw new Error(message ?? 'Impossible de traiter la demande');
            }

            return body as ForgotPasswordResponse;
        },
    });
}
