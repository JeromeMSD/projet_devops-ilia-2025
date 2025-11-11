from functools import wraps
from flask import request, jsonify, g
from .utils import verify_token
from .redis_client import get_redis_client
from .models.user import User
import os

USER_KEY = os.getenv("USER_KEY")

def auth_required(roles=None):
    """
    Décorateur Flask pour sécuriser les routes.
    - Vérifie le token JWT.
    - Vérifie que le token est bien celui stocké dans Redis.
    - Optionnellement, vérifie le rôle (roles=['ADMIN', 'SRE']).
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return jsonify({"error": "En-tête Authorization manquante"}), 403
            parts = auth_header.split()
            if parts[0] != "Bearer":
                return jsonify({"error": "Cle Bearer manquante dans l'en-tête Authorization"}), 403
            if len(parts) == 1 or not parts[1].strip():
                return jsonify({"error": "Token manquant"}), 403
            else:
                try:
                    token = parts[1].strip()
                    payload = verify_token(token)
                except Exception as error:
                    print(error)
                    return jsonify({"error": "Token invalide"}), 403
                # Si le token est expiré, ton verify_token renvoie une string (id_user)
                if isinstance(payload, str):
                    return jsonify({"error": "Token expiré, reconnectez-vous"}), 403
                # Vérification Redis
                user_id = payload["id_user"]
                user_role = payload.get("role", "").upper()
                redis_client = get_redis_client()
                raw = redis_client.get(f"{USER_KEY}{user_id}")
                if not raw:
                    return jsonify({"error": "Token invalide, Utilisateur introuvable"}), 403
                user = User.from_redis_to_user(raw)
                if user.token != token:
                    return jsonify({"error": "Token révoqué"}), 403
                # Vérification du rôle si précisé
                if roles and user_role not in [r.upper() for r in roles]:
                    return jsonify({"error": f"Permission refusée, Vous devez etre {[role.upper() for role in roles]} "}), 403
                # Stockage de l'utilisateur dans le contexte Flask
                g.current_user = user
                return fn(*args, **kwargs)
        return wrapper
    return decorator
