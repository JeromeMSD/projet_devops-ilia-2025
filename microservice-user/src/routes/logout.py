import os
from flask import Blueprint, jsonify, Response
from flask_cors import cross_origin
from dotenv import load_dotenv
import redis

from ..auth import auth_required
from ..redis_client import get_redis_client
from flask import g

load_dotenv()

USER_KEY = os.getenv('USER_KEY')

logout_bp = Blueprint('logout', __name__)


@logout_bp.route('/logout', methods=['POST'])
@cross_origin()
@auth_required()
def logout_route() -> tuple[Response, int]:
    """
    Déconnecte un utilisateur en vidant son token dans Redis.
    
    Cette route nécessite une authentification valide (token JWT dans le header Authorization).
    Après la déconnexion, le token de l'utilisateur est vidé ("") dans Redis, 
    ce qui révoque sa session active.
    
    Headers:
        Authorization (str): Bearer token JWT
    
    Returns:
        flask.Response: Une réponse HTTP JSON contenant l'état de la déconnexion.
            - 200 OK : Déconnexion réussie.
            - 403 Forbidden : Token manquant, invalide, expiré ou révoqué.
            - 500 Internal Server Error : Erreur d'exécution inattendue.
    """
    try:
        # L'utilisateur courant est déjà vérifié par @auth_required
        # et stocké dans g.current_user
        current_user = g.current_user
        
        # Obtenir le client Redis
        redis_client = get_redis_client()
        
        # Vérifier la connexion Redis
        if redis_client is None:
            return jsonify({
                "error": "Database connection unavailable"
            }), 500
        
        # Vider le token dans Redis avec gestion d'erreur
        try:
            current_user.token = ""
            redis_client.set(
                name=f"{USER_KEY}{current_user.id_user}",
                value=current_user.to_redis()
            )
            
        except redis.RedisError as e:
            print(f"Erreur Redis lors de la déconnexion: {e}")
            return jsonify({
                "error": "Cannot update user session in database"
            }), 500
        
        return jsonify({
            'message': 'Utilisateur déconnecté avec succès'
        }), 200
        
    except redis.ConnectionError as e:
        print(f"Erreur de connexion Redis: {e}")
        return jsonify({
            "error": "Cannot connect to database"
        }), 500
        
    except Exception as error:
        print(f"Erreur inattendue lors de la déconnexion: {error}")
        return jsonify({
            'error': 'Une erreur inattendue est survenue lors de la déconnexion',
            'details': str(error)
        }), 500