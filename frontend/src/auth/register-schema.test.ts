import { describe, expect, it } from 'vitest';

import { registerSchema } from './register-schema';

describe('registerSchema', () => {
    it('validates required fields and constraints', () => {
        const result = registerSchema.safeParse({
            firstname: '',
            lastname: ' ',
            email: 'bad',
            password: '123',
            role: 'guest',
        });

        expect(result.success).toBe(false);
        if (!result.success) {
            expect(result.error.issues.map((issue) => issue.message)).toEqual([
                'Prénom requis',
                'Nom requis',
                'Email invalide',
                'Le mot de passe doit contenir au moins 6 caractères, une majuscule et un chiffre',
                'Rôle invalide',
            ]);
        }
    });

    it('returns trimmed values with uppercase role', () => {
        const parsed = registerSchema.parse({
            firstname: '  Alice ',
            lastname: ' Doe  ',
            email: ' alice@example.com ',
            password: '  Password1  ',
            role: 'ADMIN',
        });

        expect(parsed).toEqual({
            firstname: 'Alice',
            lastname: 'Doe',
            email: 'alice@example.com',
            password: 'Password1',
            role: 'ADMIN',
        });
    });
});
