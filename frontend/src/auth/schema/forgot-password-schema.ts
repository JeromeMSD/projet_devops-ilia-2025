import { z } from 'zod';

export const forgotPasswordSchema = z.object({
    email: z.string()
        .trim()
        .min(1, 'Adresse email requise')
        .pipe(z.email({ message: 'Email invalide' })),
});

export type ForgotPasswordValues = z.infer<typeof forgotPasswordSchema>;
