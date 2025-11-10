import useAuthUser from 'react-auth-kit/hooks/useAuthUser';

import type { AuthUser } from '@/auth/types';

export function Dashboard() {
    const user = useAuthUser<AuthUser | null>();

    if (!user) {
        return (
            <section className="rounded-2xl border border-dashed p-6 text-center text-sm border-amber-400 bg-amber-50 text-amber-900">
                <p>Impossible de récupérer vos informations utilisateur.</p>
            </section>
        );
    }

    return (
        <section className="w-full max-w-3xl space-y-6">
            <header className="rounded-2xl border p-6 shadow-sm border-slate-200 bg-white text-slate-900">
                <p className="text-sm uppercase tracking-[0.35em] text-[#2563eb]">Tableau de bord</p>
                <h1 className="mt-2 text-3xl font-semibold">Bienvenue, {user.username}</h1>
                <p className="mt-2 text-slate-600">Vous êtes connecté avec le rôle <strong>{user.role}</strong>.</p>
            </header>

            <div className="grid gap-4 md:grid-cols-2">
                <article className="rounded-2xl border p-4 border-slate-200 bg-white text-sm text-slate-600">
                    <h2 className="text-base font-semibold text-slate-900">Profil</h2>
                    <dl className="mt-3 space-y-2">
                        <div>
                            <dt className="text-xs uppercase tracking-wide text-slate-500">Identifiant</dt>
                            <dd className="text-slate-900">{user.user_id}</dd>
                        </div>
                        <div>
                            <dt className="text-xs uppercase tracking-wide text-slate-500">Email</dt>
                            <dd className="text-slate-900">{user.email}</dd>
                        </div>
                    </dl>
                </article>
                <article className="rounded-2xl border p-4 border-slate-200 bg-white text-sm text-slate-600">
                    <h2 className="text-base font-semibold text-slate-900">Statut</h2>
                    <p className="mt-3">
                        Compte créé le{' '}
                        <span className="font-medium text-slate-900">
                            {new Date(user.created_at).toLocaleDateString()}
                        </span>
                    </p>
                </article>
            </div>
        </section>
    );
}
