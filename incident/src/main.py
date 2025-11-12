import os
from flask import Flask, jsonify

# Initialise l'application Flask
app = Flask(__name__)

# Stockage temporaire (avant Redis), comme suggéré dans le sujet, on utilise un dictionnaire pour simuler notre base de données au début.

db = {
    "incidents": {}
}

# Routes du microservice 'incidents'

@app.route('/api/v1/incidents/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "ok",
        "service": "incidents"
    }), 200


@app.route('/api/v1/incidents', methods=['GET'])
def get_incidents():

    # Pour l'instant, on retourne juste la liste des valeurs de notre dictionnaire d'incidents.
    incidents_list = list(db["incidents"].values())
    return jsonify(incidents_list), 200


# Lancement du serveur
if __name__ == '__main__':
    # On récupère le port depuis les variables d'environnement, avec 5000 comme valeur par défaut.
    port = int(os.environ.get('PORT', 5000))
    # 0.0.0.0 = accessible depuis l'extérieur du conteneur, debug=True = recharge auto quand on sauve
    app.run(host='0.0.0.0', port=port, debug=True)
