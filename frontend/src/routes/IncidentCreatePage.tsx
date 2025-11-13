import React from 'react';

function IncidentCreatePage() {
    return (
        <div className="p-10 max-w-3xl mx-auto space-y-8 bg-white shadow-xl rounded-lg border border-gray-200">
        
            {/* Titre Principal */}
            <h1 className="text-3xl font-extrabold text-gray-800 border-b pb-4">
                Signaler un Nouvel Incident
            </h1>

            {/* Formulaire */}
            <form className="space-y-6">
            
                {/* Champ: Titre de l'incident */}
                <div>
                    {}
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
                    />
                </div>

                {/* Bouton de Soumission */}
                <div className="pt-4">
                    {/* C'est ce <button> que le test "RED"  recherche
                    (grâce au texte "Signaler l'incident").
                    */}
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