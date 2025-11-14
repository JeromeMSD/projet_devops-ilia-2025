import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';

import { About } from './About';

describe('About', () => {
    it('renders the hero copy and guidance steps', () => {
        render(<About />);

        expect(screen.getByRole('heading', { name: /A quick word on this starter/i })).toBeInTheDocument();
        expect(screen.getByText(/How to add more pages/i)).toBeInTheDocument();
        expect(screen.getAllByRole('listitem')).toHaveLength(3);
        expect(screen.getByText(/React 19/i)).toBeInTheDocument();
    });
});
