from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import redis

from ..auth import auth_required
from ..models.user import User
from src.redis_client import get_redis_client
from flask import g

update_user_bp = Blueprint('update_user', __name__)

@update_user_bp.route('/users/<string:user_id>', methods=['PUT'])
@cross_origin()
@auth_required(roles=['ADMIN', 'SRE'])
def update_user(user_id: str):
    """
    Route pour modifier un utilisateur.
    
    Args:
        user_id (str): ID de l'utilisateur à modifier
    
    Returns:
        JSON: Utilisateur modifié
    
    Responses:
        200: Utilisateur modifié avec succès
        403: Accès non autorisé
        404: Utilisateur non trouvé
        500: Erreur serveur
    """
    try:
        # Vérifier les données de la requête
        if not request.json:
            return jsonify({"error": "Données JSON requises"}), 400
        
        # Obtenir le client Redis
        redis_client = get_redis_client()
        if redis_client is None:
            return jsonify({"error": "Database connection unavailable"}), 500

        # Vérifier que l'utilisateur existe
        user_key = f"user:{user_id}"
        user_data = redis_client.get(user_key)
        
        if not user_data:
            return jsonify({"error": "Utilisateur non trouvé"}), 404

        # Désérialiser l'utilisateur
        user = User.from_redis_to_user(user_data)
        
        # Mettre à jour les champs autorisés
        update_data = request.json
        
        if 'firstname' in update_data:
            user.firstname = update_data['firstname']
        
        if 'lastname' in update_data:
            user.lastname = update_data['lastname']
        
        if 'role' in update_data:
            # Validation du rôle
            valid_roles = ['USER', 'SRE', 'ADMIN']
            if update_data['role'] not in valid_roles:
                return jsonify({"error": f"Rôle invalide. Rôles valides: {valid_roles}"}), 400
            user.role = update_data['role']

        # Sauvegarder dans Redis
        redis_client.set(user_key, user.to_redis())

        return jsonify({
            "message": "Utilisateur modifié avec succès",
            "user": user.to_json()
        }), 200

    except redis.ConnectionError:
        return jsonify({"error": "Cannot connect to database"}), 500

    except Exception as e:
        print(f"Erreur inattendue dans update_user: {e}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500