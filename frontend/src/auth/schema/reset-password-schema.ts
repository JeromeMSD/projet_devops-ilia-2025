import { z } from 'zod';

const PASSWORD_REQUIREMENTS_MESSAGE = 'Le mot de passe doit contenir au moins 6 caractères, une majuscule et un chiffre';

export const resetPasswordSchema = z.object({
    reset_token: z.string()
        .trim()
        .min(1, 'Token requis'),
    new_password: z.string()
        .trim()
        .regex(/^(?=.*[A-Z])(?=.*\d).{6,}$/, PASSWORD_REQUIREMENTS_MESSAGE),
});

export type ResetPasswordValues = z.infer<typeof resetPasswordSchema>;
