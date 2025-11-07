import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';

describe('App', () => {
    it('renders logos, heading and text', () => {
        render(<App/>);

        expect(screen.getByAltText(/Vite logo/i)).toBeInTheDocument();
        expect(screen.getByAltText(/React logo/i)).toBeInTheDocument();

        expect(
            screen.getByRole('heading', { level: 1, name: /Vite \+ React/i }),
        ).toBeInTheDocument();

        expect(
            screen.getByText(/Click on the Vite and React logos to learn more/i),
        ).toBeInTheDocument();
    });

    it('increments count when button is clicked', async () => {
        render(<App/>);

        const user = userEvent.setup();
        const button = screen.getByRole('button', { name: /count is 0/i });

        await user.click(button);

        expect(
            screen.getByRole('button', { name: /count is 1/i }),
        ).toBeInTheDocument();
    });
});