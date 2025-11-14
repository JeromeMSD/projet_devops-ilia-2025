import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router';

import { NotFound } from './NotFound';

describe('NotFound', () => {
    it('shows the 404 message and a link back to home', () => {
        render(
            <MemoryRouter>
                <NotFound />
            </MemoryRouter>,
        );

        expect(screen.getByText(/Lost in the grid/i)).toBeInTheDocument();
        expect(screen.getByRole('link', { name: /Back to Home/i })).toHaveAttribute('href', '/');
    });
});
