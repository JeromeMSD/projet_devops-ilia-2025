import { render, screen } from '@testing-library/react';
import { HomePage } from '../../pages/HomePage';
import { mockServices } from '../../utils/mockData';

describe('Home page', () => {
    it('renders all services', () => {
        render(<HomePage />);
        mockServices.forEach(service => {
            expect(screen.getByText(service.name)).toBeInTheDocument();
        });
    });
});
