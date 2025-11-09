import React from 'react';
import { render, screen } from '@testing-library/react';
import ProfilePage from './ProfilePage'; 
vi.mock('../mocks/mockData', () => ({
    mockUser: {
        firstname: "Sebastien",
        lastname: "Lacroix",
        email: "seb.lacroix@test.com", 
        role: "SRE"
    }
}));
test('afficher le nom complet de l\'utilisateur', () => {
    render(<ProfilePage />);
    const userNameElement = screen.getByText(/Sebastien Lacroix/i); 
    expect(userNameElement).toBeInTheDocument();
});
test('afficher l\'email et le rôle de l\'utilisateur', () => {
    render(<ProfilePage />);
    const emailElement = screen.getByText(/seb.lacroix@test.com/i);
    const roleElement = screen.getByText(/Rôle: SRE/i);
    expect(emailElement).toBeInTheDocument();
    expect(roleElement).toBeInTheDocument();
});