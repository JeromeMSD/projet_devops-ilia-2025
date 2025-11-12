import { describe, expect, it } from 'vitest';

import { loginSchema } from './login-schema.ts';

describe('loginSchema', () => {
    it('rejects empty credentials', () => {
        const result = loginSchema.safeParse({ email: ' ', password: '' });

        expect(result.success).toBe(false);
        if (!result.success) {
            expect(result.error.issues.map((issue) => issue.message)).toEqual([
                'Adresse email requise',
                'Mot de passe requis',
            ]);
        }
    });

    it('trims values before validation', () => {
        const parsed = loginSchema.parse({ email: '  alice@example.com  ', password: '  secret  ' });

        expect(parsed).toEqual({ email: 'alice@example.com', password: 'secret' });
    });
});
