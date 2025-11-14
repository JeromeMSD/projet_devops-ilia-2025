import { useMemo } from 'react';
import ServiceCard from '../components/ServiceCard';
import { mockServices } from '../utils/mockData';

export function Home() {
    const overall = useMemo(() => {
        if (mockServices.some(s => s.status === 'down')) return { text: 'Incident en cours', level: 'danger' };
        if (mockServices.some(s => s.status === 'partial')) return { text: 'Dégradé', level: 'warn' };
        return { text: 'Tous les systèmes opérationnels', level: 'ok' };
    }, []);

    const bannerClass = overall.level === 'danger'
        ? 'bg-red-600 text-white'
        : overall.level === 'warn'
            ? 'bg-yellow-500 text-black'
            : 'bg-green-600 text-white';

    return (
        <main className="max-w-6xl mx-auto">
            <header className="mb-8">
                <h1 className="text-4xl font-extrabold mb-2 text-slate-800 dark:text-blue-500">
                    PolyStatus
                </h1>
                <p className="text-slate-600 dark:text-slate-300">Vue d’ensemble des microservices</p>

                <div className={`mt-4 inline-flex items-center gap-4 px-4 py-2 rounded ${bannerClass}`}>
                    <span className="font-semibold">{overall.text}</span>
                    <span className="text-sm opacity-80">({mockServices.length} services surveillés)</span>
                </div>
            </header>

            <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {mockServices.map(s => (
                    <ServiceCard key={s.id} service={s} />
                ))}
            </section>
        </main>
    );
}
