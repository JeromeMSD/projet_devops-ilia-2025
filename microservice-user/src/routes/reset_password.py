import os
import re
from flask import Blueprint, request, jsonify, Response
from flask_cors import cross_origin
from dotenv import load_dotenv
import redis

from ..redis_client import get_redis_client
from ..utils import hash_password, verify_token
from ..models.user import User

load_dotenv()

USER_KEY = os.getenv('USER_KEY')
RESET_TOKEN_KEY = os.getenv('RESET_TOKEN_KEY', 'reset:token:')

reset_password_bp = Blueprint('reset_password', __name__)


@reset_password_bp.route('/reset-password', methods=['POST'])
@cross_origin()
def reset_password_route() -> tuple[Response, int]:
    """
    Réinitialise le mot de passe d'un utilisateur avec un token de reset.
    Cette route permet à un utilisateur de définir un nouveau mot de passe
    en utilisant le token de réinitialisation reçu via /forgot-password.
    Le token est à usage unique et expire après 30 minutes.
    Body JSON:
        reset_token (str): Le token JWT de réinitialisation
        new_password (str): Le nouveau mot de passe (min 6 chars, 1 maj, 1 chiffre)
    Returns:
        flask.Response: Une réponse HTTP JSON.
            - 200 OK : Mot de passe réinitialisé avec succès
            - 400 Bad Request : Champs manquants ou mot de passe invalide
            - 403 Forbidden : Token invalide, expiré ou déjà utilisé
            - 500 Internal Server Error : Erreur serveur
    """
    try:
        # Obtenir le client Redis
        redis_client = get_redis_client()
        if redis_client is None:
            return jsonify({"error": "Database connection unavailable"}), 500
        # Extraction du body
        data = request.get_json(silent=True)
        if not data:
            return jsonify({
                'error': 'Corps de la requête vide ou invalide'
            }), 400
        # Vérification des champs requis
        if 'reset_token' not in data or not data['reset_token']:
            return jsonify({
                'error': 'Le champ reset_token est requis'
            }), 400
        if 'new_password' not in data or not data['new_password']:
            return jsonify({
                'error': 'Le champ new_password est requis'
            }), 400
        reset_token = data['reset_token']
        new_password = data['new_password']
        # Validation du nouveau mot de passe (même règles que register)
        password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{6,}$"
        if not re.search(password_regex, new_password):
            return jsonify({
                'error': 'Le mot de passe doit contenir au moins 6 caractères, une majuscule, une minuscule et un chiffre'
            }), 400
        # Vérifier que le token existe dans Redis avec gestion d'erreur
        try:
            user_id_bytes = redis_client.get(f"{RESET_TOKEN_KEY}{reset_token}")
        except redis.RedisError as e:
            print(f"Erreur Redis lors de la vérification du token reset: {e}")
            return jsonify({
                'error': 'Erreur de base de données lors de la vérification du token'
            }), 500
        if not user_id_bytes:
            return jsonify({
                'error': 'Token de réinitialisation invalide ou expiré'
            }), 403
        user_id = user_id_bytes.decode('utf-8') if isinstance(user_id_bytes, bytes) else user_id_bytes
        # Vérifier la validité du JWT (signature et expiration)
        try:
            payload = verify_token(reset_token)
            # Si le token est expiré, verify_token retourne un string (user_id)
            if isinstance(payload, str):
                # Nettoyer le token expiré de Redis avec gestion d'erreur
                try:
                    redis_client.delete(f"{RESET_TOKEN_KEY}{reset_token}")
                except redis.RedisError as e:
                    print(f"Erreur Redis lors de la suppression du token expiré: {e}")
                    # On continue car le token est déjà expiré de toute façon
                return jsonify({
                    'error': 'Token de réinitialisation expiré'
                }), 403
            # Vérifier que l'user_id du token correspond à celui dans Redis
            if payload.get('id_user') != user_id:
                return jsonify({
                    'error': 'Token de réinitialisation invalide'
                }), 403
        except Exception as error:
            print(f"Erreur lors de la vérification du token: {error}")
            return jsonify({
                'error': 'Token de réinitialisation invalide'
            }), 403
        # Récupérer l'utilisateur depuis Redis avec gestion d'erreur
        try:
            user_data = redis_client.get(f"{USER_KEY}{user_id}")
        except redis.RedisError as e:
            print(f"Erreur Redis lors de la récupération de l'utilisateur {user_id}: {e}")
            return jsonify({
                'error': 'Erreur de base de données lors de la récupération de l\'utilisateur'
            }), 500
        if not user_data:
            return jsonify({
                'error': 'Utilisateur introuvable'
            }), 404
        user = User.from_redis_to_user(user_data)
        # Hasher et mettre à jour le mot de passe
        user.password = hash_password(new_password)
        # Révoquer le token de session actuel pour forcer une reconnexion
        user.token = ""
        # Sauvegarder dans Redis avec gestion d'erreur
        try:
            redis_client.set(name=f"{USER_KEY}{user_id}", value=user.to_redis())
        except redis.RedisError as e:
            print(f"Erreur Redis lors de la sauvegarde de l'utilisateur {user_id}: {e}")
            return jsonify({
                'error': 'Erreur de base de données lors de la mise à jour du mot de passe'
            }), 500
        # Supprimer le token de reset (usage unique) avec gestion d'erreur
        try:
            redis_client.delete(f"{RESET_TOKEN_KEY}{reset_token}")
        except redis.RedisError as e:
            print(f"Erreur Redis lors de la suppression du token reset: {e}")
            # On continue car l'utilisateur a déjà été mis à jour
        return jsonify({
            'message': 'Mot de passe réinitialisé avec succès'
        }), 200
    except redis.ConnectionError as e:
        print(f"Erreur de connexion Redis: {e}")
        return jsonify({
            "error": "Cannot connect to database"
        }), 500
    except Exception as error:
        print(f"Erreur inattendue dans reset_password: {error}")
        return jsonify({
            'error': 'Une erreur inattendue est survenue',
            'details': str(error)
        }), 500
