export function About() {
    const panelClasses = 'border-slate-200 bg-white text-slate-700';

    return (
        <section className="mx-auto flex max-w-5xl flex-col gap-8">
            {/* Section principale */}
            <div className={`rounded-3xl border p-8 shadow-[0_20px_80px_-40px_rgba(15,23,42,1)] ${panelClasses}`}>
                <p className="text-sm uppercase tracking-[0.35em] text-[#2563eb]">À propos</p>
                <h1 className="mt-4 text-3xl font-semibold md:text-4xl">
                    Bienvenue sur le dashboard des microservices
                </h1>
                <p className="mt-4 text-base opacity-80">
                    Cette interface vous permet de visualiser rapidement l'état de tous les microservices de l'application.
                    Chaque service est représenté par une carte avec son statut actuel, sa description, et des liens vers ses pages spécifiques.
                    L'objectif est de centraliser l'information pour faciliter la supervision et la gestion de vos services.
                </p>
            </div>

            {/* Section fonctionnalités */}
            <div className="grid gap-5 md:grid-cols-2">
                <article className={`rounded-2xl border p-6 ${panelClasses}`}>
                    <h2 className="text-xl font-semibold">Fonctionnalités principales</h2>
                    <ul className="mt-4 list-disc space-y-2 pl-5 text-sm opacity-80">
                        <li>Visualiser l'état en temps réel de tous les microservices</li>
                        <li>Accéder rapidement aux pages détaillées de chaque service</li>
                        <li>Surveiller les incidents et la disponibilité globale de l'application</li>
                        <li>Recevoir des informations sur les services cloud externes via le CSP Ingestor</li>
                        <li>Identifier les fonctionnalités expérimentales via le Flags Service</li>
                    </ul>
                </article>

                <article className={`rounded-2xl border p-6 ${panelClasses}`}>
                    <h2 className="text-xl font-semibold">Pour qui ?</h2>
                    <p className="mt-4 text-sm opacity-80">
                        Ce dashboard est destiné aux développeurs et aux équipes DevOps pour :
                    </p>
                    <ul className="mt-2 list-disc pl-5 text-sm opacity-80">
                        <li>Surveiller la santé des microservices</li>
                        <li>Réagir rapidement aux incidents</li>
                        <li>Maintenir une vision globale de l'application</li>
                        <li>Faciliter la collaboration entre les équipes</li>
                    </ul>
                </article>
            </div>
        </section>
    );
}
