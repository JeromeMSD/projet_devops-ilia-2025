import { render, screen } from '@testing-library/react';
import type { ServiceCard } from '../ServiceCard';
import type { Service } from '../../utils/mockData';

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
        render(<ServiceCard service={mockService} />);
        expect(screen.getByText('Test Service')).toBeInTheDocument();
        expect(screen.getByText('Un service pour tester')).toBeInTheDocument();
    });

    it('contains link if href is provided', () => {
        render(<ServiceCard service={mockService} />);
        const link = screen.getByRole('link');
        expect(link).toHaveAttribute('href', '/test');
    });

    it('displays status correctly', () => {
        render(<ServiceCard service={mockService} />);
        expect(screen.getByText(/operational/i)).toBeInTheDocument();
    });
});
