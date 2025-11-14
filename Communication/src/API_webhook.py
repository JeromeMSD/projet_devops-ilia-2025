
from flask import Flask, request, jsonify
from datetime import datetime
from src.config_redis import redis_client


app = Flask(__name__)

@app.route("/api/v1/webhooks", methods=["POST"])
def register_webhook():
    """
    Enregistrer un webhook pour notifier un système externe lors de nouveaux événements.
    """
    data = request.get_json()

    # Vérification des champs requis
    if not data or 'url' not in data or 'event_type' not in data:
        return jsonify({"error": "Champs 'url' et 'event_type' requis"}), 400

    # Génération d’un ID unique via Redis
    webhook_id = redis_client.incr("webhook_id")

    webhook = {
        "id": webhook_id,
        "url": data["url"],
        "event_type": data["event_type"],
        "date": datetime.now().date().isoformat()
    }

    # Sauvegarde dans Redis
    redis_client.lpush("webhooks", str(webhook))

    # Réponse JSON
    return jsonify({
        "message": "Webhook enregistré avec succès",
        "webhook": webhook
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
