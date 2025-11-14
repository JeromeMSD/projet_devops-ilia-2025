import type { ReactElement, ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router';
import useIsAuthenticated from 'react-auth-kit/hooks/useIsAuthenticated';

type ProtectedRouteProps = {
    children: ReactNode;
};

export function ProtectedRoute({ children }: ProtectedRouteProps): ReactElement {
    const isAuthenticated = useIsAuthenticated();
    const location = useLocation();

    if (!isAuthenticated) {
        return <Navigate to="/login" state={{ from: location }} replace/>;
    }

    return <>{children}</>;
}
