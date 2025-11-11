import { describe, expect, it } from 'vitest';

import { loginSchema } from './login-schema';

describe('loginSchema', () => {
    it('rejects empty credentials', () => {
        const result = loginSchema.safeParse({ username: ' ', password: '' });

        expect(result.success).toBe(false);
        if (!result.success) {
            expect(result.error.issues.map((issue) => issue.message)).toEqual([
                'Nom d\'utilisateur requis',
                'Mot de passe requis',
            ]);
        }
    });

    it('trims values before validation', () => {
        const parsed = loginSchema.parse({ username: '  alice  ', password: '  secret  ' });

        expect(parsed).toEqual({ username: 'alice', password: 'secret' });
    });
});
