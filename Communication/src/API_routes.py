from datetime import datetime
from config_redis import redis_client
from flask import jsonify, Flask, request

app = Flask(__name__)
app.config["DEBUG"] = True

#Route test
@app.route("/api/v1/test", methods=['GET'])
def test():
    test1 = {"id":1, "name":"Aude", "Lastname":"Javel"}
    return jsonify(test1)

#Route annonce
@app.route('/api/v1/public/announce', methods=['POST'])
def CreateAnnouncement():

    data = request.get_json()

    #Compteur redis pour incrémenter l'id à chaque annonce crée
    announce_id = redis_client.incr('announce_id')

    announce1 = {
        "id": announce_id,
        "message": data["message"],
        "etat": data["etat"],
        "date":datetime.now().date().isoformat()
    }

    redis_client.lpush("annonces", json.dumps(announce1))

    #Retourne l'annonce et la confirmation en json
    return jsonify({
        "message":"Annonce bien enregistrée",
        "announce": announce1
    }),201


#données fictives simulées pour tester le get : 
INCIDENTS = [
    {
        "id": 1,
        "title": "Panne du serveur principal",
        "status": "en cours",
        "messages": [
            {"timestamp": "2025-11-11T09:00:00Z", "text": "Incident détecté."},
            {"timestamp": "2025-11-11T09:30:00Z", "text": "Équipe en intervention."}
        ]
    },
    {
        "id": 2,
        "title": "Maintenance planifiée API",
        "status": "résolu",
        "messages": [
            {"timestamp": "2025-11-10T12:00:00Z", "text": "Maintenance terminée."}
        ]
    }
]
# route get status
@app.route("/api/v1/public/status", methods=["GET"])
def get_public_status():
    return jsonify({
        "status": "success",
        "count": len(INCIDENTS),
        "data": INCIDENTS
    }), 200

@app.route("/api/v1/email", methods=["POST"])
def send_email():
    """
    Route 3: Simule l'envoi d'un email.
    Accepte un JSON avec 'to', 'subject', et 'body'.
    """
    data = request.get_json()

    if not data or "to" not in data or "subject" not in data or "body" not in data:
        return jsonify({"erreur": "Données manquantes: 'to', 'subject', 'body' requis"}), 400

    to_email = data["to"]
    subject = data["subject"]
    body = data["body"]

    print("="*30)
    print(f"SIMULATION D'ENVOI D'EMAIL")
    print(f"À: {to_email}")
    print(f"Sujet: {subject}")
    print("="*30)
    return jsonify({
        "message": "Email simulé envoyé avec succès",
        "email_data": data
    }), 200 

app.run()


