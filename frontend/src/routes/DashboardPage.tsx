import { type MockIncident, mockIncidents } from '@/mocks/mockData';
import type { AuthUser } from '@/auth/types.ts';
import useAuthUser from 'react-auth-kit/hooks/useAuthUser';

function DashboardPage() {
    const user = useAuthUser<AuthUser | null>();

    if (!user) {
        return (
            <section
                className="rounded-2xl border border-dashed p-6 text-center text-sm border-amber-400 bg-amber-50 text-amber-900">
                <p>Impossible de récupérer vos informations utilisateur.</p>
            </section>
        );
    }

    const criticalIncidents = mockIncidents.filter(
        (incident: MockIncident) => incident.severity.toLowerCase() === 'critique',
    );
    const criticalCount = criticalIncidents.length;

    const assignedIncidents = mockIncidents.filter(
        (incident: MockIncident) => incident.assignee_id === user.id_user,
    );
    return (
        // Conteneur centré
        <div className="p-10 max-w-6xl mx-auto space-y-10 min-h-screen">

            <h1 className="text-4xl font-extrabold text-gray-800 border-b pb-4">
                Tableau de Bord SRE
            </h1>
            {/* Résumé des Critiques (Simule un composant Stat Card) */}
            <div className="p-6 rounded-xl shadow-2xl bg-white border-l-8 border-red-600">
                <p className="text-lg text-gray-500">Incidents Critiques en Cours</p>
                <p className="text-5xl font-extrabold text-red-600 mt-2">
                    {criticalCount}
                </p>
            </div>
            {/* Liste des Incidents Assignés */}
            <div className="pt-4">
                <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                    Vos Incidents Assignés ({assignedIncidents.length})
                </h2>
                <ul className="space-y-4">
                    {assignedIncidents.map((incident: MockIncident) => (
                        <li
                            key={incident.id}
                            // Style d'un élément de liste cliquable
                            className="p-4 border border-gray-100 rounded-md bg-white shadow-md hover:shadow-lg transition-shadow cursor-pointer border-l-4"
                        >
                            <p className="font-semibold text-lg text-gray-900">{incident.title}</p>
                            <p className="text-sm text-gray-500 mt-1">Sévérité: {incident.severity.toUpperCase()}</p>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default DashboardPage;