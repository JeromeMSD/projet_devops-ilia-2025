const features = [
    {
        title: 'Ready-to-go routing',
        description: 'React Router 7 is already configured with a sample 404 route so you can plug in new pages quickly.',
        icon: '🧭',
    },
    {
        title: 'Tailwind styling',
        description: 'Tailwind CSS 4 powers utility-first styles. Keep things minimal or scale up as the UI grows.',
        icon: '🎨',
    },
    {
        title: 'Vite dev server',
        description: 'Hot reloads, instant feedback, and production builds on demand thanks to Vite + TypeScript.',
        icon: '⚡️',
    },
];

export function Home() {
    const chips = 'rounded-full border px-4 py-2 text-sm backdrop-blur border-slate-200 text-slate-600 bg-white/80';

    return (
        <section className="mx-auto flex max-w-5xl flex-col gap-10">
            <div
                className="overflow-hidden rounded-3xl border p-8 shadow-[0_20px_80px_-40px_rgba(15,23,42,1)] md:p-10 border-slate-200 bg-white text-slate-600 shadow-slate-200/70">
                <p className="text-sm uppercase tracking-[0.35em] text-[#2563eb]">
                    Starter kit
                </p>
                <h1 className={`mt-4 text-4xl font-semibold md:text-5xl text-slate-900`}>
                    A friendly React + Vite baseline
                </h1>
                <p className="mt-4 max-w-2xl text-lg">
                    This tiny showcase keeps the focus on routing, layout, and a sprinkle of styling. Duplicate the
                    section, wire a route, and you are off to the races.
                </p>

                <div className="mt-8 flex flex-wrap gap-3 text-sm">
                    <span className={chips}>React 19 + TypeScript</span>
                    <span className={chips}>Vite dev server</span>
                    <span className={chips}>Tailwind CSS utilities</span>
                </div>
            </div>

            <div className="grid gap-6 md:grid-cols-3">
                {features.map((feature) => (
                    <article key={feature.title}
                             className="rounded-2xl border p-5 text-sm shadow-[0_15px_45px_-40px_rgba(15,23,42,1)] border-slate-200 bg-white text-slate-600 shadow-slate-200/60">
                        <div className="text-2xl">{feature.icon}</div>
                        <h2 className={`mt-4 text-lg font-semibold text-slate-900`}>{feature.title}</h2>
                        <p className="mt-2">{feature.description}</p>
                    </article>
                ))}
            </div>

            <div className="rounded-2xl border border-dashed p-6 text-sm border-slate-300 bg-white/80 text-slate-600">
                <p className={`text-base font-semibold text-slate-900`}>Try it out</p>
                <p className="mt-2">
                    Create a route inside `src/routes`, register it in `src/App.tsx`, and drop your component into the
                    layout. The styles above are intentionally lightweight so you can morph them into whatever your team
                    needs.
                </p>
            </div>
        </section>
    );
}
