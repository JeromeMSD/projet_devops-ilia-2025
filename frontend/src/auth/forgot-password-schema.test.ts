import { describe, expect, it } from 'vitest';

import { forgotPasswordSchema } from './forgot-password-schema';

describe('forgotPasswordSchema', () => {
    it('validates email presence and format', () => {
        const result = forgotPasswordSchema.safeParse({ email: 'not-an-email' });

        expect(result.success).toBe(false);
        if (!result.success) {
            expect(result.error.issues.map((issue) => issue.message)).toEqual(['Email invalide']);
        }
    });

    it('trims email input', () => {
        const parsed = forgotPasswordSchema.parse({ email: '  user@example.com  ' });

        expect(parsed).toEqual({ email: 'user@example.com' });
    });
});
