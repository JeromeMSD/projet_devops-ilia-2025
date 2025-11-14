import { NavLink } from 'react-router';

export function Navbar() {
    const linkClasses = ({ isActive }: { isActive: boolean }) =>
        [
            'inline-flex items-center rounded-full px-4 py-2 text-sm font-medium transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 hover:text-slate-900 hover:bg-slate-900/5 focus-visible:outline-slate-800/40',
            isActive
                ? 'bg-slate-900/5 text-slate-900 shadow-inner shadow-slate-900/10'
                : 'text-slate-600',
        ].join(' ');

    return (
        <header className={`sticky top-0 z-10 backdrop-blur border-b border-slate-200/70 bg-white/80 text-slate-800`}>
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
                            <NavLink to="/incidents" className={linkClasses}>
                            Incidents
                        </NavLink>
                    </nav>
                </div>
            </div>
        </header>
    );
}
