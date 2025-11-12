import { describe, expect, it } from 'vitest';

import { resetPasswordSchema } from './reset-password-schema';

describe('resetPasswordSchema', () => {
    it('validates required token and password strength', () => {
        const result = resetPasswordSchema.safeParse({ reset_token: ' ', new_password: 'weak' });

        expect(result.success).toBe(false);
        if (!result.success) {
            expect(result.error.issues.map((issue) => issue.message)).toEqual([
                'Token requis',
                'Le mot de passe doit contenir au moins 6 caractères, une majuscule et un chiffre',
            ]);
        }
    });

    it('trims values before validation', () => {
        const parsed = resetPasswordSchema.parse({
            reset_token: '  token ',
            new_password: ' Password1 ',
        });

        expect(parsed).toEqual({
            reset_token: 'token',
            new_password: 'Password1',
        });
    });
});
