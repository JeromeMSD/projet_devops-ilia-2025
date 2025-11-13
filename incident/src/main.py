import os
import time
import uuid
import redis
from flask import Flask, jsonify, request
from redis_link import *

app = Flask(__name__)

@app.route('/api/v1/incidents/health', methods=['GET'])
def health_check():
    # Vérifie la connexion au serveur Redis et retourne le statut de santé du microservice
    try:
        if r.ping():
            return jsonify({
                "status": "ok",
                "service": "incidents",
                "redis": "connected"
            }), 200
        else:
            return jsonify({
                "status": "error",
                "service": "incidents",
                "redis": "not responding"
            }), 500
    except redis.exceptions.ConnectionError as e:
        return jsonify({
            "status": "error",
            "service": "incidents",
            "redis": f"connection error: {e}"
        }), 500


@app.route('/api/v1/incidents', methods=['POST'])
def create_incident():
    # Crée un nouvel incident à partir des données JSON reçues dans la requête
    # Génère un ID unique, initialise les champs de l'incident et sauvegarde dans Redis
    data = request.get_json()
    if not data or 'title' not in data or 'sev' not in data:
        return jsonify({"error": "Requête invalide: 'title' et 'sev' sont requis."}), 400

    new_id = f"INC-{uuid.uuid4().hex[:6].upper()}"
    new_incident = {
        "id": new_id,
        "title": data.get("title"),
        "sev": data.get("sev"),
        "services": data.get("services", []),
        "summary": data.get("summary", ""),
        "status": "open",
        "started_at": int(time.time()),
        "commander": None
    }

    saveJSONFile(new_incident)
    return jsonify(new_incident), 201


@app.route('/api/v1/incidents', methods=['GET'])
def get_incidents():
    # Récupère tous les incidents depuis Redis et applique les filtres facultatifs 'commander' et 'status'
    filters = request.args
    incidents_list = []

    keys = r.keys("INC-*")  # Récupère toutes les clés d'incidents dans Redis
    for key in keys:
        obj = loadJSONFile(key)  # Charge l'objet JSON depuis Redis
        if obj:
            incidents_list.append(obj)

    # Filtre par 'commander' si spécifié
    if 'commander' in filters:
        commander_id = filters.get('commander')
        incidents_list = [inc for inc in incidents_list if inc.get('commander') == commander_id]

    # Filtre par 'status' si spécifié
    if 'status' in filters:
        status = filters.get('status')
        incidents_list = [inc for inc in incidents_list if inc.get('status') == status]

    return jsonify(incidents_list), 200


@app.route("/api/v1/incidents/<incident_id>", methods=["GET"])
def get_incident_by_id(incident_id):
    # Récupère un incident spécifique depuis Redis à partir de son ID
    # Retourne une erreur 404 si l'incident n'existe pas
    incident = loadJSONFile(incident_id)
    if not incident:
        return jsonify({"error": "Incident not found"}), 404
    return jsonify(incident), 200





@app.route('/api/v1/incidents/<id>/timeline', methods=['PUT'])
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
    incident["timeline"].append(
        {"type": data["type"], "message": data["message"]})
    db["incidents"][id] = incident
    return jsonify(incident), 200


@app.route('/api/v1/incidents/<id>/postmortem', methods=['PUT'])
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


@app.route('/api/v1/incidents/<id>/status', methods=['PUT'])
def update_incident_status(id):
    incident = db["incidents"].get(id)
    if not incident:
        return jsonify({"error": "Incident not found"}), 404

    data = request.get_json()
    if not data or "status" not in data:
        return jsonify({"error": "Missing status"}), 400

    if data["status"] not in ["open", "mitigated", "resolved"]:
        return jsonify({"error": "Invalid status"}), 400

    incident["status"] = data["status"]
    db["incidents"][id] = incident


@app.route("/api/v1/incidents/<incident_id>/assign", methods=["PUT"])
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


if __name__ == '__main__':
    # Démarre l'application Flask sur le port défini par la variable d'environnement PORT ou 5000 par défaut
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)