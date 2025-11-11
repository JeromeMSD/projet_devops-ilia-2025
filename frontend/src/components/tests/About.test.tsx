import { render, screen } from '@testing-library/react';
import { About } from '../../routes/About';


describe('About page', () => {
    it('renders main title', () => {
        render(<About />);
        expect(screen.getByText(/bienvenue sur le dashboard/i)).toBeInTheDocument();
    });

    it('renders feature list', () => {
        render(<About />);
        expect(screen.getByText(/visualiser l'état en temps réel/i)).toBeInTheDocument();
        expect(screen.getByText(/accéder rapidement aux pages détaillées/i)).toBeInTheDocument();
    });
});
