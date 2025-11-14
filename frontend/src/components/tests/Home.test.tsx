import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { Home } from '../../routes/Home';
import { mockServices } from '../../utils/mockData';

describe('Home page', () => {
    it('renders all services', () => {
        render(
            <MemoryRouter>
                <Home />
            </MemoryRouter>
        );

        mockServices.forEach(service => {
            expect(screen.getByText(service.name)).toBeInTheDocument();
        });
    });
});
