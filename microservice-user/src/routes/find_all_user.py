from flask import Blueprint, jsonify
from flask_cors import cross_origin
import redis

from ..auth import auth_required
from ..models.user import User
from src.redis_client import get_redis_client

get_all_users_bp = Blueprint('find_all_user', __name__)


@get_all_users_bp.route(rule='/users', methods=['GET'])
@cross_origin()
@auth_required(roles=['ADMIN', 'SRE'])
def find_all_users():
    """
    Route pour récupérer tous les utilisateurs stockés dans Redis.
    Returns:
        JSON: Liste de tous les utilisateurs avec leur nombre total
    Responses :
        200: Liste des utilisateurs récupérée avec succès
        500: Erreur serveur (problème Redis ou autre)
    """
    try:
        # Obtenir le client Redis
        redis_client = get_redis_client()
        # Vérifier la connexion Redis
        if redis_client is None:
            return jsonify({
                "error": "Database connection unavailable"
            }), 500
        # Récupérer toutes les clés des utilisateurs
        # Pattern: tous les utilisateurs ont des clés qui commencent par "user:"
        user_keys = redis_client.keys('user:*')
        users_list = []
        # Parcourir toutes les clés et récupérer les utilisateurs
        for key in user_keys:
            try:
                # Récupérer l'objet user depuis Redis (bytes)
                user_data = redis_client.get(key)
                if user_data:
                    # Convertir de Redis vers objet User
                    user = User.from_redis_to_user(user_data)
                    # Ajouter la version JSON (sans password) à la liste
                    users_list.append(user.to_json())
            except Exception as e:
                print(f"Erreur lors de la récupération de l'utilisateur {key}: {e}")
                continue
        # Retourner la liste avec le nombre total
        return jsonify({
            "count": len(users_list),
            "users": users_list
        }), 200
    except redis.ConnectionError:
        return jsonify({
            "error": "Cannot connect to database"
        }), 500
    except Exception as e:
        print(f"Erreur inattendue dans find_all_users: {e}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500
