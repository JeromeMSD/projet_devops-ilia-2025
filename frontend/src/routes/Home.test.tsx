import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router';
import { Home } from './Home.tsx';
import { mockServices } from '../utils/mockData.ts';

describe('Home page', () => {
    it('renders all services', () => {
        render(
            <MemoryRouter>
                <Home />
            </MemoryRouter>,
        );

        mockServices.forEach(service => {
            expect(screen.getByText(service.name)).toBeInTheDocument();
        });
    });
});
