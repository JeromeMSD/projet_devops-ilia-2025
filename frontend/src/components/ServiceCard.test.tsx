import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router';
import ServiceCard from './ServiceCard.tsx';
import type { Service } from '../utils/mockData.ts';

const mockService: Service = {
    id: 'svc-test',
    name: 'Test Service',
    description: 'Un service pour tester',
    status: 'operational',
    icon: 'User',
    href: '/test',
};

describe('ServiceCard', () => {
    it('renders service name and description', () => {
        render(
            <MemoryRouter>
                <ServiceCard service={mockService} />
            </MemoryRouter>,
        );
        expect(screen.getByText('Test Service')).toBeInTheDocument();
        expect(screen.getByText('Un service pour tester')).toBeInTheDocument();
    });

    it('contains link if href is provided', () => {
        render(
            <MemoryRouter>
                <ServiceCard service={mockService} />
            </MemoryRouter>,
        );
        const link = screen.getByRole('link');
        expect(link).toHaveAttribute('href', '/test');
    });

    it('displays status correctly', () => {
        render(
            <MemoryRouter>
                <ServiceCard service={mockService} />
            </MemoryRouter>,
        );
        expect(screen.getByText(/operational/i)).toBeInTheDocument();
    });
});
