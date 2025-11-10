from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import redis

from ..auth import auth_required
from ..models.user import User
from src.redis_client import get_redis_client

find_users_by_role_bp = Blueprint('find_users_by_role', __name__)

@find_users_by_role_bp.route('/users/role/<string:role>', methods=['GET'])
@cross_origin()
@auth_required(roles=['ADMIN', 'SRE'])
def find_users_by_role(role: str):
    """
    Route pour récupérer les utilisateurs filtrés par rôle.
    
    Args:
        role (str): Le rôle pour filtrer les utilisateurs (ex: 'ADMIN', 'USER', 'SRE')
    
    Returns:
        JSON: Liste des utilisateurs ayant le rôle spécifié avec leur nombre total
    
    Responses:
        200: Liste des utilisateurs récupérée avec succès
        403: Accès non autorisé (token manquant, invalide ou permissions insuffisantes)
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

        # Normaliser le rôle (majuscules pour la cohérence)
        normalized_role = role.upper()

        # Récupérer toutes les clés des utilisateurs
        user_keys = redis_client.keys('user:*')

        users_list = []

        # Parcourir toutes les clés et récupérer les utilisateurs avec le rôle spécifié
        for key in user_keys:
            try:
                # Récupérer l'objet user depuis Redis (bytes)
                user_data = redis_client.get(key)

                if user_data:
                    # Convertir de Redis vers objet User
                    user = User.from_redis_to_user(user_data)
                    
                    # Filtrer par rôle (comparaison insensible à la casse)
                    if user.role.upper() == normalized_role:
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
        print(f"Erreur inattendue dans find_users_by_role: {e}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500