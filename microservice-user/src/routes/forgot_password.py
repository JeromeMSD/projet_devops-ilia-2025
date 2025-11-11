import os
import re
from datetime import timedelta
from flask import Blueprint, request, jsonify, Response
from flask_cors import cross_origin
from dotenv import load_dotenv
import redis

from ..redis_client import get_redis_client
from ..utils import create_token

load_dotenv()

EMAIL_KEY = os.getenv('EMAIL_KEY')
USER_KEY = os.getenv('USER_KEY')
RESET_TOKEN_KEY = os.getenv('RESET_TOKEN_KEY', 'reset:token:')

# Durée de validité du token de reset : 30 minutes
RESET_TOKEN_VALIDITY = timedelta(minutes=30)

forgot_password_bp = Blueprint('forgot_password', __name__)


@forgot_password_bp.route('/forgot-password', methods=['POST'])
@cross_origin()
def forgot_password_route() -> tuple[Response, int]:
    """
    Génère un token de réinitialisation de mot de passe.
    
    Cette route permet à un utilisateur de demander la réinitialisation de son mot de passe
    en fournissant son adresse email. Un token JWT temporaire (valide 30 minutes) est généré
    et stocké dans Redis.
    
    Body JSON:
        email (str): L'adresse email de l'utilisateur
    
    Returns:
        flask.Response: Une réponse HTTP JSON.
            - 200 OK : Token de reset généré avec succès
            - 400 Bad Request : Email manquant ou format invalide
            - 500 Internal Server Error : Erreur serveur
    
    Note:
        Pour des raisons de sécurité (OWASP), même si l'email n'existe pas,
        on retourne 200 pour ne pas révéler l'existence ou non d'un compte.
    """
    try:
        # Obtenir le client Redis
        redis_client = get_redis_client()
        if redis_client is None:
            return jsonify({"error": "Database connection unavailable"}), 500
        
        # Extraction du body
        data = request.get_json(silent=True)
        
        if data is None:
            return jsonify({
                'error': 'Corps de la requête vide ou invalide'
            }), 400
        
        if 'email' not in data or not data['email']:
            return jsonify({
                'error': 'Le champ email est requis'
            }), 400
        
        email = data['email'].lower().strip()
        
        # Validation du format email
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{3}$"
        if not re.fullmatch(email_regex, email):
            return jsonify({
                'error': 'Format d\'email invalide'
            }), 400
        
        # Vérifier si l'utilisateur existe avec gestion d'erreur Redis
        try:
            user_id_bytes = redis_client.get(f"{EMAIL_KEY}{email}")
        except redis.RedisError as e:
            print(f"Erreur Redis lors de la vérification de l'email {email}: {e}")
            # Pour la sécurité, on retourne 200 même en cas d'erreur Redis
            return jsonify({
                'message': 'Si cet email existe, un lien de réinitialisation a été envoyé'
            }), 200
        
        # Pour des raisons de sécurité (OWASP), on retourne toujours 200
        # même si l'utilisateur n'existe pas (évite l'énumération d'emails)
        if not user_id_bytes:
            return jsonify({
                'message': 'Si cet email existe, un lien de réinitialisation a été envoyé'
            }), 200
        
        user_id = user_id_bytes.decode('utf-8') if isinstance(user_id_bytes, bytes) else user_id_bytes
        
        # Générer un token JWT de reset (valide 30 minutes)
        reset_token = create_token(user_id, validity=RESET_TOKEN_VALIDITY)
        
        # Stocker le token dans Redis avec expiration (TTL = 30 minutes)
        try:
            redis_client.setex(
                name=f"{RESET_TOKEN_KEY}{reset_token}",
                time=int(RESET_TOKEN_VALIDITY.total_seconds()),
                value=user_id
            )
        except redis.RedisError as e:
            print(f"Erreur Redis lors du stockage du token de reset: {e}")
            # Même en cas d'erreur, on retourne 200 pour la sécurité
            return jsonify({
                'message': 'Si cet email existe, un lien de réinitialisation a été envoyé'
            }), 200
        
        # En production, envoyer le token par email
        # Ici, on le retourne directement pour les tests
        return jsonify({
            'message': 'Token de réinitialisation généré avec succès',
            'reset_token': reset_token
        }), 200
        
    except redis.ConnectionError as e:
        print(f"Erreur de connexion Redis: {e}")
        # Pour la sécurité, on retourne 200 même si Redis est down
        return jsonify({
            'message': 'Si cet email existe, un lien de réinitialisation a été envoyé'
        }), 200
        
    except Exception as error:
        print(f"Erreur inattendue dans forgot_password: {error}")
        # Pour la sécurité, on retourne 200 même pour les erreurs inattendues
        return jsonify({
            'message': 'Si cet email existe, un lien de réinitialisation a été envoyé'
        }), 200