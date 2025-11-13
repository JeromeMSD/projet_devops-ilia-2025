import React, { useState } from 'react';

function IncidentCreatePage() {
    const [title, setTitle] = useState('');
    const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const incidentData = {
        title: title,
      sev: 2 
    };
    try {
        await fetch('http://localhost:8081/api/incidents', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(incidentData)
        });
        console.log('Incident signalé avec succès !');
        setTitle('');

    } catch (error) {
        console.error("Erreur lors de la soumission de l'incident:", error);
    }
    };

    return (
    // Conteneur de page stylisé
    <div className="p-10 max-w-3xl mx-auto space-y-8 bg-white shadow-xl rounded-lg border border-gray-200">
        
        <h1 className="text-3xl font-extrabold text-gray-800 border-b pb-4">
            Signaler un Nouvel Incident
        </h1>

        {/* 7. Lie la fonction 'handleSubmit' à l'événement 'onSubmit' du formulaire */}
        <form className="space-y-6" onSubmit={handleSubmit}>
            
            <div>
                <label 
                    htmlFor="title" 
                    className="block text-sm font-medium text-gray-700 mb-1"
                >
                    Titre de l'incident
                </label>
                <input
                    type="text"
                    id="title"
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    placeholder="Ex: Latence sur l'API EU-West"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />
            </div>

            <div className="pt-4">
                <button
                    type="submit"
                    className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                    Signaler l'incident
                </button>
            </div>

        </form>
    </div>
    );
}
export default IncidentCreatePage;