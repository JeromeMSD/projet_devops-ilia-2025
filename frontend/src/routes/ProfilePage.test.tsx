import React from 'react';
import { render, screen } from '@testing-library/react';
import ProfilePage from './ProfilePage'; 
import { vi } from 'vitest';

vi.mock('../mocks/mockData', () => ({
    mockUser: {
        firstname: "Sebastien", 
        lastname: "Lacroix",
    }
}));

test(' afficher le nom complet de l\'utilisateur', () => {
    render(<ProfilePage />);
    
    const userNameElement = screen.getByText(/Sebastien Lacroix/i); 
    
    expect(userNameElement).toBeInTheDocument();
});