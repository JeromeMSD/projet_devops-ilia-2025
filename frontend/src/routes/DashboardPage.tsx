import React from 'react';
import { mockIncidents , mockUser} from '../mocks/mockData';
import type { MockIncident } from '../mocks/mockData'; 
function DashboardPage() {
    const criticalIncidents = mockIncidents.filter(
        (incident: MockIncident) => incident.severity.toLowerCase() === 'critique'
    );
    const criticalCount = criticalIncidents.length;
    const assignedIncidents = mockIncidents.filter(
        (incident: MockIncident) => incident.assignee_id === mockUser.user_id
    );
    return (
        <div className="p-4">
            <h1>Dashboard SRE</h1>
            {/* Résumé */}
            <p className="text-xl mb-6">
                {criticalCount} Incidents Critiques en cours
            </p>   
            <hr />
            {/* Liste filtrée */}
            <h2>Vos Incidents Assignés ({assignedIncidents.length})</h2>
            <ul>
                {assignedIncidents.map((incident: MockIncident) => (
                    <li key={incident.id}>
                        {incident.title} - Sévérité: {incident.severity}
                    </li>
                ))}
            </ul>
        </div>
    );
}
export default DashboardPage;