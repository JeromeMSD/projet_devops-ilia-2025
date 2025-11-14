from flask import Blueprint, jsonify
from flask_cors import cross_origin
from src.redis_client import get_redis_client, USER_KEY
from src.redis_client import get_redis_client, USER_KEY

import json

# Définition du blueprint
one_user_bp = Blueprint('one_user_bp', __name__)

@one_user_bp.route('/users/<id_user>', methods=['GET'])
@cross_origin()
def get_user_by_id(id_user):
    redis_client = get_redis_client()
    if redis_client is None:
        return jsonify({"error": "Impossible de se connecter à Redis"}), 500

    key = f"{USER_KEY}{id_user}"
    if not redis_client.exists(key):
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    user_data = redis_client.get(key)
    try:
        user_json = json.loads(user_data)
    except Exception as e:
        return jsonify({"error": f"Erreur lecture utilisateur: {e}"}), 500

    return jsonify({"message": "Utilisateur trouvé", "user": user_json}), 200
