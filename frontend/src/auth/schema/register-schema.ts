import { z } from 'zod';

export const roles = ['USER', 'SRE', 'ADMIN'] as const;

const PASSWORD_REQUIREMENTS_MESSAGE = 'Le mot de passe doit contenir au moins 6 caractères, une majuscule et un chiffre';

export const registerSchema = z.object({
    firstname: z.string()
        .trim()
        .min(1, 'Prénom requis'),
    lastname: z.string()
        .trim()
        .min(1, 'Nom requis'),
    email: z.string()
        .trim()
        .min(1, 'Adresse email requise')
        .pipe(z.email({ message: 'Email invalide' })),
    password: z.string()
        .trim()
        .regex(/^(?=.*[A-Z])(?=.*\d).{6,}$/, PASSWORD_REQUIREMENTS_MESSAGE),
    role: z.enum(roles, {
        error: () => ({ message: 'Rôle invalide' }),
    }),
});

export type RegisterFormValues = z.infer<typeof registerSchema>;
