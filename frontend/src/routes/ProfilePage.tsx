import React from 'react';
import { mockUser , mockIncidents } from '../mocks/mockData';
function ProfilePage() {
    return (
        <div>
        <h1>Profil de {mockUser.username}</h1>
        <p>{mockUser.email}</p>
        <p>Rôle: {mockUser.role}</p>
        <hr />
        <h2>Incidents assignés</h2>
        <ul>
            {mockIncidents.map(incident => (
            <li key={incident.id}>
                {incident.title}
            </li>
            ))}
        </ul>
        </div>
    );
}
export default ProfilePage;