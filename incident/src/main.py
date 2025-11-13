import os
import uuid
import time
from flask import Flask, jsonify, request

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


@app.route('/api/v1/incidents', methods=['POST'])
def create_incident():  # Crée un nouvel incident

    # On récupere le JSON, pour l'instant basé sur le modèl du swagger de base
    data = request.get_json()

    # Validation (le Swagger demande "title" et "sev")
    # Verifie que title et sev on était initié car obligatoire d'après le swagger
    if not data or 'title' not in data or 'sev' not in data:
        return jsonify({"error": "Requête invalide: 'title' et 'sev' sont requis."}), 400

    # Construire l'objet incident (basé sur schéma "Incident")
    # Génère un ID d'incident court, unique et lisible. ex : INC-153F5C
    new_id = f"INC-{uuid.uuid4().hex[:6].upper()}"
    new_incident = {
        "id": new_id,
        "title": data.get("title"),
        "sev": data.get("sev"),
        "services": data.get("services", []),  # "services" est optionnel
        "summary": data.get("summary", ""),   # "summary" est optionnel
        "status": "open",                     # "open" par défaut
        "started_at": int(time.time()),       # Timestamp UNIX
        "commander": None                     # Pas de "commander" assigné au début
    }

    # Sauvegarde dans notre base de données "dictionnaire"
    db["incidents"][new_id] = new_incident

    # Retourne l'incident créé avec un statut 201
    return jsonify(new_incident), 201


@app.route('/api/v1/incidents', methods=['GET'])
def get_incidents():  # Lister tous les incidents, gérer les filtres

    # Récupérer les filtres de l'URL (query parameters)
    filters = request.args

    # Commencer avec la liste complète (On fait une copie pour ne pas modifier l'original)
    incidents_list = list(db["incidents"].values())

    # On va appliquer les filtres un par un

    # Filtre commander
    if 'commander' in filters:
        commander_id = filters.get('commander')
        new_filtered_list = []
        for inc in incidents_list:
            if inc.get('commander') == commander_id:
                new_filtered_list.append(inc)
        incidents_list = new_filtered_list

    # Filtre status
    if 'status' in filters:
        status = filters.get('status')
        new_filtered_list = []
        for inc in incidents_list:
            if inc.get('status') == status:
                new_filtered_list.append(inc)
        incidents_list = new_filtered_list

    return jsonify(incidents_list), 200

@app.route('/api/v1/incidents/<id>/timeline', methods=['POST'])
def add_timeline_event(id):
    incident = db["incidents"].get(id)
    if not incident:
        return jsonify({"error": "Incident not found"}), 404

    data = request.get_json()
    if not data or "type" not in data or "message" not in data:
        return jsonify({"error": "Missing type or message"}), 400

    if "timeline" not in incident:
        incident["timeline"] = []

    # Ajouter l'événement à la timeline
    incident["timeline"].append({"type": data["type"], "message": data["message"]})
    db["incidents"][id] = incident
    return jsonify(incident), 200

@app.route('/api/v1/incidents/<id>/postmortem', methods=['POST'])
def add_postmortem(id):
    incident = db["incidents"].get(id)
    if not incident:
        return jsonify({"error": "Incident not found"}), 404

    data = request.get_json()
    required_fields = ["what_happened", "root_cause", "action_items"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing postmortem fields"}), 400

    incident["postmortem"] = {
        "what_happened": data["what_happened"],
        "root_cause": data["root_cause"],
        "action_items": data["action_items"]
    }

    db["incidents"][id] = incident
    return jsonify(incident), 200

@app.route("/api/v1/incidents/<incident_id>", methods=["GET"])
def get_incident_by_id(incident_id):
    incident = db["incidents"].get(incident_id)
    if not incident:
        return jsonify({"error": "Incident not found"}), 404
    return jsonify(incident), 200


@app.route("/api/v1/incidents/<incident_id>/assign", methods=["POST"])
def assign_incident(incident_id):
    incident = db["incidents"].get(incident_id)
    if not incident:
        return jsonify({"error": "Incident not found"}), 404

    data = request.get_json() or {}
    commander = data.get("commander")
    if not commander:
        return jsonify({"error": "Missing field 'commander'"}), 400

    incident["commander"] = commander
    db["incidents"][incident_id] = incident  # update local store

    return jsonify(incident), 200


# Lancement du serveur
if __name__ == '__main__':
    # On récupère le port depuis les variables d'environnement, avec 5000 comme valeur par défaut.
    port = int(os.environ.get('PORT', 5000))
    # 0.0.0.0 = accessible depuis l'extérieur du conteneur, debug=True = recharge auto quand on sauve
    app.run(host='0.0.0.0', port=port, debug=True)
