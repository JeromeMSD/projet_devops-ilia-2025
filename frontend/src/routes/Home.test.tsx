import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';

import { Home } from './Home';

describe('Home', () => {
    it('renders the hero message, highlight chips, and feature cards', () => {
        render(<Home />);

        expect(screen.getByRole('heading', { name: /A friendly React \+ Vite baseline/i })).toBeInTheDocument();
        expect(screen.getByText(/Ready-to-go routing/i)).toBeInTheDocument();
        expect(screen.getByText(/Tailwind CSS utilities/i)).toBeInTheDocument();
        expect(screen.getByText(/Try it out/i)).toBeInTheDocument();
        expect(screen.getByText(/Create a route inside `src\/routes`/i)).toBeInTheDocument();
    });
});
