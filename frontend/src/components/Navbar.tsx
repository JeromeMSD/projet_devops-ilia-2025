import { NavLink, useNavigate } from 'react-router';
import useIsAuthenticated from 'react-auth-kit/hooks/useIsAuthenticated';
import useSignOut from 'react-auth-kit/hooks/useSignOut';
import useAuthUser from 'react-auth-kit/hooks/useAuthUser';

import type { AuthUser } from '@/auth/types';

export function Navbar() {
    const navigate = useNavigate();
    const isAuthenticated = useIsAuthenticated();
    const signOut = useSignOut();
    const authUser = useAuthUser<AuthUser | null>();

    const linkClasses = ({ isActive }: { isActive: boolean }) =>
        [
            'inline-flex items-center rounded-full px-4 py-2 text-sm font-medium transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 hover:text-slate-900 hover:bg-slate-900/5 focus-visible:outline-slate-800/40',
            isActive
                ? 'bg-slate-900/5 text-slate-900 shadow-inner shadow-slate-900/10'
                : 'text-slate-600',
        ].join(' ');

    const handleSignOut = () => {
        signOut();
        navigate('/login');
    };

    return (
        <header className="sticky top-0 z-10 border-b border-slate-200/70 bg-white/80 text-slate-800 backdrop-blur">
            <div className="mx-auto flex max-w-5xl flex-col gap-4 px-4 py-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                    <p className="text-xs uppercase tracking-[0.2em] opacity-70">Vite + Router</p>
                    <p className="text-lg font-semibold text-[#2563eb]">
                        Frontend Playground
                    </p>
                </div>

                <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-end">
                    {isAuthenticated && authUser ? (
                        <div className="text-right text-xs uppercase tracking-[0.2em] text-slate-500">
                            Connecté en tant que
                            <p className="text-base font-semibold normal-case tracking-normal text-slate-900">
                                {authUser.username}
                            </p>
                        </div>
                    ) : null}

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
                                <button
                                    type="button"
                                    onClick={handleSignOut}
                                    className="inline-flex items-center rounded-full border border-transparent bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-slate-800/40"
                                >
                                    Déconnexion
                                </button>
                            </>
                        ) : (
                            <NavLink to="/login" className={linkClasses}>
                                Login
                            </NavLink>
                        )}
                    </nav>
                </div>
            </div>
        </header>
    );
}
