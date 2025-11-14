import { Link } from 'react-router';

export function NotFound() {

    return (
        <section
            className="mx-auto flex max-w-md flex-col gap-4 rounded-2xl border p-8 text-center shadow-[0_25px_70px_-60px_rgba(15,23,42,1)] border-slate-200 bg-white text-slate-600 shadow-slate-200/60">
            <p className="text-sm uppercase tracking-[0.3em] text-[#2563eb]">
                404
            </p>
            <h1 className={`text-3xl font-semibold text-slate-900`}>Lost in the grid</h1>
            <p>We could not find that page. Maybe it has not been wired up yet.</p>
            <Link to="/"
                  className="inline-flex items-center justify-center rounded-full border px-5 py-2 text-sm font-medium transition border-slate-300 text-slate-700 hover:bg-slate-900/5">
                ← Back to Home
            </Link>
        </section>
    );
}
