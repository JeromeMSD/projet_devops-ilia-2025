import { NavLink, useNavigate } from 'react-router';
import useIsAuthenticated from 'react-auth-kit/hooks/useIsAuthenticated';
import useAuthUser from 'react-auth-kit/hooks/useAuthUser';

import type { AuthUser } from '@/auth/types';
import { useLogout } from '@/auth/useLogout';
import { Spinner } from '@/components/ui/spinner.tsx';
import { Avatar, AvatarFallback } from '@/components/ui/avatar.tsx';

export function Navbar() {
    const navigate = useNavigate();
    const isAuthenticated = useIsAuthenticated();
    const authUser = useAuthUser<AuthUser | null>();
    const logout = useLogout();
    const displayName = authUser
        ? [authUser.firstname, authUser.lastname].filter(Boolean).join(' ').trim() || authUser.email
        : '';
    const initials = authUser
        ? [authUser.firstname, authUser.lastname]
            .filter(Boolean)
            .map((name) => name[0].toUpperCase())
            .join('')
        : '';
    const avatarLabel = displayName ? `Profil de ${displayName}` : 'Profil utilisateur';

    const linkClasses = ({ isActive }: { isActive: boolean }) =>
        [
            'inline-flex items-center rounded-full px-4 py-2 text-sm font-medium transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 hover:text-slate-900 hover:bg-slate-900/5 focus-visible:outline-slate-800/40',
            isActive
                ? 'bg-slate-900/5 text-slate-900 shadow-inner shadow-slate-900/10'
                : 'text-slate-600',
        ].join(' ');

    const handleSignOut = () => {
        logout.mutate(undefined, {
            onSettled: () => {
                navigate('/login');
            },
        });
    };

    const handleProfileNavigation = () => {
        navigate('/me');
    };

    return (
        <header className="sticky top-0 z-10 border-b border-slate-200/70 bg-white/80 text-slate-800 backdrop-blur">
            <div
                className="mx-auto flex max-w-5xl flex-col gap-4 px-4 py-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                    <p className="text-xs uppercase tracking-[0.2em] opacity-70">Vite + Router</p>
                    <p className="text-lg font-semibold text-[#2563eb]">
                        Frontend Playground
                    </p>
                </div>

                <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-end">
                    <nav className="flex items-center gap-2">
                        <NavLink to="/" className={linkClasses} end>
                            Home
                        </NavLink>
                        <NavLink to="/about" className={linkClasses}>
                            About
                        </NavLink>
                        {isAuthenticated ? (
                            <>
                                <NavLink to="/dashboard" className={linkClasses}>
                                    Dashboard
                                </NavLink>
                                {authUser ? (
                                    <button
                                        type="button"
                                        onClick={handleProfileNavigation}
                                        aria-label={avatarLabel}
                                        className="inline-flex items-center justify-center rounded-full border border-transparent bg-slate-100 p-0.5 focus-visible:outline focus-visible:outline-offset-2 focus-visible:outline-slate-800/40"
                                    >
                                        <Avatar className="size-8">
                                            <AvatarFallback className="text-xs font-semibold uppercase">
                                                {initials || '?'}
                                            </AvatarFallback>
                                        </Avatar>
                                    </button>
                                ) : null}
                                <div className="flex flex-col items-stretch">
                                    <button
                                        type="button"
                                        onClick={handleSignOut}
                                        disabled={logout.isPending}
                                        className="inline-flex items-center rounded-full border border-transparent bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-800 disabled:opacity-60 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-slate-800/40"
                                    >
                                        {logout.isPending && <Spinner />}
                                        {logout.isPending ? 'Déconnexion...' : 'Déconnexion'}
                                    </button>
                                    {logout.error instanceof Error && (
                                        <p className="mt-1 text-xs font-medium text-red-600" role="status">
                                            {logout.error.message}
                                        </p>
                                    )}
                                </div>
                            </>
                        ) : (
                            <>
                                <NavLink to="/login" className={linkClasses}>
                                    Login
                                </NavLink>
                                <NavLink to="/register" className={linkClasses}>
                                    Register
                                </NavLink>
                            </>
                        )}
                    </nav>
                </div>
            </div>
        </header>
    );
}
