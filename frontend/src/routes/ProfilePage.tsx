import React from 'react';
import { mockUser, mockIncidents } from '../mocks/mockData';
function ProfilePage() {
    return (
        <div className="p-10 max-w-4xl mx-auto space-y-8 bg-gray-50 min-h-screen">
            
            {/* Titre Principal */}
            <h1 className="text-4xl font-extrabold text-gray-800 border-b pb-4">
                Mon Profil SRE
            </h1>

            {/* Section 1: Carte de l'Utilisateur (Simule un composant Card/Avatar) */}
            <div className="flex items-center space-x-6 p-6 border border-gray-200 rounded-xl shadow-lg bg-white">
                
                {/* Avatar / Initiale (avec des classes simulant un cercle) */}
                <div className="flex items-center justify-center w-16 h-16 rounded-full bg-blue-500 text-white text-2xl font-bold">
                    {mockUser.username.charAt(0)}
                </div>

                {/* Détails du Profil */}
                <div>
                    <h2 className="text-2xl font-bold text-gray-900">
                        {mockUser.username}
                    </h2>
                    <p className="text-md text-gray-500">
                        {mockUser.email}
                    </p>
                    
                    {/* Rôle (Simule un Badge) */}
                    <span className="mt-2 inline-flex items-center px-3 py-1 text-xs font-semibold rounded-full tracking-wide 
                                    bg-red-500 text-white uppercase shadow-md">
                        {mockUser.role}
                    </span>
                </div>
            </div>
            
            {/* Section 2: Liste des Incidents Assignés */}
            <div className="pt-4">
                <h3 className="text-2xl font-semibold text-gray-800 mb-4">
                    Incidents Assignés ({mockIncidents.length})
                </h3>
                
                {/* Liste d'éléments stylisés */}
                <ul className="space-y-4">
                    {mockIncidents.map(incident => (
                        <li 
                            key={incident.id} 
                            className="p-4 border-l-4 border-yellow-500 rounded-md bg-white shadow-sm hover:shadow-lg transition-shadow cursor-pointer"
                        >
                            <p className="font-semibold text-lg text-gray-900">
                                {incident.title}
                            </p>
                            <p className="text-sm text-gray-500 mt-1">
                                ID: {incident.id}
                            </p>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}
export default ProfilePage;