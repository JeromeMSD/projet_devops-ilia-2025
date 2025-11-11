import { render } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import ProfilePage from './ProfilePage';

describe('ProfilePage', () => {
    it('renders the placeholder container', () => {
        const { container } = render(<ProfilePage/>);
        expect(container.querySelector('div')).toBeInTheDocument();
    });
});
