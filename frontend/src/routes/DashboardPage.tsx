import React from 'react';
import { mockIncidents } from '../mocks/mockData';
import type { MockIncident } from '../mocks/mockData'; 
function DashboardPage() {
    const criticalIncidents = mockIncidents.filter(
        incident => incident.severity.toLowerCase() === 'critique' 
    );
    const criticalCount = criticalIncidents.length;
    return (
        <div className="p-4">
            <h1>Dashboard SRE</h1>
            <p className="text-xl">
                {criticalCount} Incidents Critiques en cours
            </p>
        </div>
    );
}
export default DashboardPage;