import { useMutation, useQueryClient } from '@tanstack/react-query';
import useSignOut from 'react-auth-kit/hooks/useSignOut';
import useAuthHeader from 'react-auth-kit/hooks/useAuthHeader';

const API_BASE_URL = import.meta.env.VITE_USER_API_URL ?? 'http://localhost:5010';

export function useLogout() {
    const signOut = useSignOut();
    const authHeader = useAuthHeader();
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async () => {
            const headers: HeadersInit = { 'Content-Type': 'application/json' };
            if (authHeader) {
                headers.Authorization = authHeader;
            }

            let response: Response;
            try {
                response = await fetch(`${API_BASE_URL}/api/v1/logout`, {
                    method: 'POST',
                    headers,
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

                throw new Error(message ?? 'Déconnexion impossible');
            }

            return body as { message?: string };
        },
        onSettled: () => {
            queryClient.removeQueries({ queryKey: ['currentUser'], exact: false });
            signOut();
        },
    });
}
