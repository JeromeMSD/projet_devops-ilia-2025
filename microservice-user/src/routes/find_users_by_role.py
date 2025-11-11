from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import redis

from ..auth import auth_required
from ..models.user import User
from src.redis_client import get_redis_client

find_users_by_role_bp = Blueprint('find_users_by_role', __name__)


@find_users_by_role_bp.route('/users', methods=['GET'])
@cross_origin()
@auth_required(roles=['ADMIN', 'SRE'])
def find_users_by_role():
    """
    Route pour récupérer tous les utilisateurs stockés dans Redis,
    avec filtrage optionnel par rôle via query parameter.
    Query params:
        role (str, optional): Le rôle pour filtrer les utilisateurs (ex: 'ADMIN', 'USER', 'SRE')
    Returns:
        JSON: Liste des utilisateurs (filtrés ou tous) avec leur nombre total
    Responses :
        200: Liste des utilisateurs récupérée avec succès
        403: Accès non autorisé (token manquant, invalide ou permissions insuffisantes)
        500: Erreur serveur (problème Redis ou autre)
    Examples:
        GET /api/v1/users → Tous les utilisateurs
        GET /api/v1/users ? Role=ADMIN → Seulement les ADMIN
        GET /api/v1/users ? role=USER → Uniquement les USER
        GET /api/v1/users ? role=SRE → Uniquement les SRE
    """
    try:
        # Obtenir le client Redis
        redis_client = get_redis_client()
        # Vérifier la connexion Redis
        if redis_client is None:
            return jsonify({
                "error": "Database connection unavailable"
            }), 500
        # Récupérer le query param 'role' (optionnel)
        role_filter = request.args.get('role', None)
        # Normaliser le rôle si fourni (majuscules pour la cohérence)
        normalized_role = role_filter.upper() if role_filter else None
        # Récupérer toutes les clés des utilisateurs avec try/except
        try:
            user_keys = redis_client.keys('user:*')
        except redis.RedisError as e:
            print(f"Erreur Redis lors de la récupération des clés: {e}")
            return jsonify({
                "error": "Cannot retrieve users from database"
            }), 500
        users_list = []
        # Parcourir toutes les clés et récupérer les utilisateurs
        for key in user_keys:
            try:
                # Récupérer l'objet user depuis Redis (bytes)
                user_data = redis_client.get(key)
                if user_data:
                    # Convertir de Redis vers objet User
                    user = User.from_redis_to_user(user_data)
                    # Filtrer par rôle si spécifié, sinon retourner tous les users
                    if normalized_role is None or user.role.upper() == normalized_role:
                        # Ajouter la version JSON (sans password) à la liste
                        users_list.append(user.to_json())
            except redis.RedisError as e:
                print(f"Erreur Redis lors de la récupération de l'utilisateur {key}: {e}")
                continue
            except Exception as e:
                print(f"Erreur lors du traitement de l'utilisateur {key}: {e}")
                continue
        # Retourner la liste avec le nombre total
        return jsonify({
            "count": len(users_list),
            "users": users_list
        }), 200
    except redis.ConnectionError as e:
        print(f"Erreur de connexion Redis: {e}")
        return jsonify({
            "error": "Cannot connect to database"
        }), 500
    except Exception as e:
        print(f"Erreur inattendue dans find_users_by_role: {e}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500
