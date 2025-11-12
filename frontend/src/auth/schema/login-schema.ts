import { z } from 'zod';

export const loginSchema = z.object({
    email: z.string()
        .trim()
        .min(1, 'Adresse email requise')
        .pipe(z.email({ message: 'Email invalide' })),
    password: z.string()
        .trim()
        .min(1, 'Mot de passe requis'),
});

export type LoginFormValues = z.infer<typeof loginSchema>;
