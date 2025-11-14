import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
import ProfilePage from '../../routes/ProfilePage';
import { vi, test, expect } from 'vitest';



// Mock du user
vi.mock('../../utils/mockData', () => ({
    mockUser: {
        firstname: 'Sebastien',
        lastname: 'Lacroix',
    },
}));

test("afficher le nom complet de l'utilisateur", () => {
    render(<ProfilePage />);
    const userNameElement = screen.getByText(/Sebastien Lacroix/i);
    expect(userNameElement).toBeInTheDocument();
});
