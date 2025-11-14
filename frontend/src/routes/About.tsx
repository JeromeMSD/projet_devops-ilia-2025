const steps = [
    'Duplicate a section in Home or create a new component under src/routes.',
    'Register your route inside App.tsx so the navbar and router know about it.',
    'Wire any shared UI inside components so future pages stay consistent.',
];

export function About() {
    const panelClasses = 'border-slate-200 bg-white text-slate-700';

    return (
        <section className="mx-auto flex max-w-5xl flex-col gap-8">
            <div className={`rounded-3xl border p-8 shadow-[0_20px_80px_-40px_rgba(15,23,42,1)] ${panelClasses}`}>
                <p className="text-sm uppercase tracking-[0.35em] text-[#2563eb]">
                    About
                </p>
                <h1 className="mt-4 text-3xl font-semibold md:text-4xl">A quick word on this starter</h1>
                <p className="mt-4 text-base opacity-80">
                    This Vite + React + Router setup tries to stay lean so the team can reason about routing, shared UI,
                    and theming without wading through extra dependencies. Swap content freely and keep the controls
                    above
                </p>
            </div>

            <div className="grid gap-5 md:grid-cols-2">
                <article className={`rounded-2xl border p-6 ${panelClasses}`}>
                    <h2 className="text-xl font-semibold">How to add more pages</h2>
                    <ul className="mt-4 list-disc space-y-2 pl-5 text-sm opacity-80">
                        {steps.map((step) => (
                            <li key={step}>{step}</li>
                        ))}
                    </ul>
                </article>

                <article className={`rounded-2xl border p-6 ${panelClasses}`}>
                    <h2 className="text-xl font-semibold">What is included</h2>
                    <div className="mt-4 flex flex-wrap gap-2 text-sm">
                        {['React 19', 'React Router 7', 'Tailwind 4', 'Vitest'].map((chip) => (
                            <span key={chip}
                                  className={`rounded-full border px-4 py-2 text-sm border-slate-200 bg-slate-50 text-slate-700`}>
                                {chip}
                            </span>
                        ))}
                    </div>
                </article>
            </div>
        </section>
    );
}
