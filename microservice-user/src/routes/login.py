import os
from dotenv import load_dotenv
from flask_cors import cross_origin
from flask import Blueprint, request, jsonify, Response
import jwt
from ..redis_client import get_redis_client
from ..models.user import User
from ..utils import verify_password, create_token, verify_token


login_bp = Blueprint('login', __name__)
EMAIL_KEY = os.getenv('EMAIL_KEY')
USER_KEY = os.getenv('USER_KEY')

load_dotenv()


@login_bp.route('/login', methods=['POST'])
@cross_origin()
def login_route() -> tuple[Response, int]:
    """
        Connecte un utilisateur et émet un JSON Web Token (JWT).
        Cette méthode est le point d'entrée pour l'authentification. Elle vérifie les
        identifiants fournis par l'utilisateur par rapport à ceux stockés dans la base
        de données Redis et gère la session active.
        Returns:
            flask.Response: Une réponse HTTP JSON contenant l'état de la connexion.
                - 200 OK : Connexion réussie, renvoie le JWT et les informations utilisateur.
                - 400 Bad Request: Corps de la requête invalide ou champs 'email'/'password' manquants.
                - 401 Unauthorized: Mot de passe incorrect.
                - 404 Not Found: L'utilisateur (email) est inexistant dans Redis.
                - 500 Internal Server Error: Erreur d'exécution inattendue.
    """
    redis_client = get_redis_client()
    try:
        # extraction du 'body' de la requête HTTP
        data: dict = request.get_json(silent=True)
        if not data:
            return jsonify({
                'error': 'Les champs email et password sont requis'
            }), 400
        elif not data.get('email'):
            return jsonify({
                'error': 'Le champ email est requis'
            }), 400
        elif not data.get('password'):
            return jsonify({
                'error': 'Le champ password est requis'
            }), 400
        else:
            email: str = data["email"]
            password: str = data["password"]
            # Recuperation de l'id de l'utilisateur a l'aide son email.
            user_id_key_bytes = redis_client.get(f"{EMAIL_KEY}{email}")
            if not user_id_key_bytes:
                return jsonify({
                    'error': 'Utilisateur inexistant'
                }), 404
            else:
                user_id: str = user_id_key_bytes.decode("utf-8") if isinstance(user_id_key_bytes, bytes) else user_id_key_bytes
                redis_object: bytes = redis_client.get(f"{USER_KEY}{user_id}")
                user_infos: User = User.from_redis_to_user(redis_object)
                # Verification du mot de passe
                if not verify_password(password, user_infos.password):
                    return jsonify({
                        'error': 'Mot de passe incorrect'
                    }), 401
                else:
                    # Creation du token et mise à jour des infos de l'utilisateur
                    token: str = create_token(user_id, user_infos.role)
                    user_infos.token = token
                    redis_client.set(name=f"{USER_KEY}{user_id}", value=user_infos.to_redis())
                    # Retour d'une réponse HTTP 200 avec les infos de l'utilisateur
                    return jsonify({
                        'user': user_infos.to_json(),
                        'message': 'Successfully logged in!'
                    }), 200
    except Exception as error:
        print(f"error {error} ")
        return jsonify({
            'message': "Une erreur inattendue est survenue, veuillez réessayer plus tard !",
            'error': str(error)
        }), 500


@login_bp.route('/verify-token', methods=['GET'])
@cross_origin()
def verify_token_route():
    """
        Vérifie la validité d'un JWT et l'état de la session dans Redis.
        Cette méthode extrait le token du header 'Authorization' et le valide contre
        trois critères : signature, expiration temporelle (via PyJWT) et révocation
        (via Redis).
        Returns:
            flask.Response: Une réponse HTTP JSON contenant l'état de la vérification.
                - 200 OK : Token valide et session active. Renvoie les informations utilisateur.
                - 403 Forbidden :
                    – Token manquant, signature invalide, ou token expiré.
                    - Si expiré, le champ 'token' est nettoyé dans Redis.
                - 500 Internal Server Error: Erreur d'exécution inattendue.
    """
    redis_client = get_redis_client()
    # Recuperation du champ Authorization dans les headers de la requête.
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "En-tête Authorization manquante"}), 403
    parts = auth_header.split()
    if parts[0] != "Bearer":
        return jsonify({"error": "Cle Bearer manquante dans l'en-tête Authorization"}), 403
    if len(parts) == 1 or not parts[1].strip():
        return jsonify({"error": "Token manquant"}), 403
    else:
        token = parts[1].strip()
        try:
            # Verification du token
            payload = verify_token(token=token)
            if not payload:
                return jsonify({'error': 'Token JWT invalide'}), 403
            else:
                # Token valide
                if type(payload) is dict:
                    user_id = payload['id_user']
                    print(user_id)
                    if redis_client.exists(f"{USER_KEY}{user_id}"):
                        user: User = User.from_redis_to_user(redis_client.get(f"{USER_KEY}{user_id}"))
                        stored_token = user.token
                        # Verification de l'intégrité du token
                        if not stored_token or stored_token == "":
                            return jsonify({'error': 'Token révoqué ou expiré, veuillez vous reconnecter !'}), 403
                        elif stored_token != token:
                            return jsonify({
                                'error': 'Token invalide ou  révoqué',
                                'message': 'Ce token aurait ete révoqué ce qui cause son invalidité'
                            }), 403
                        else:
                            return jsonify(
                                {
                                    'message': "Utilisateur connecté",
                                    'user': user.to_json(),
                                }
                            ), 200
                    else:
                        return jsonify({
                            'error': 'Token invalide',
                            'message': 'L\'utilisateur associé a ce token est inexistant'
                        }), 403
                # Token expire
                elif type(payload) is str:
                    user_id = payload
                    if redis_client.exists(f"{USER_KEY}{user_id}"):
                        user = User.from_redis_to_user(redis_client.get(f"{USER_KEY}{user_id}"))
                        user.token = ""
                        redis_client.set(name=f"{USER_KEY}{user_id}", value=user.to_redis())
                        return jsonify({
                            'error': 'Token expiré, veuillez vous reconnecter'
                        }), 403
                    else:
                        return jsonify({
                            'error': 'Token invalide',
                            'message': 'L\'utilisateur associé a ce token est inexistant'
                        }), 403
                else:
                    return jsonify({'error': 'Erreur inattendue'}), 500
        # Gestion des erreurs
        except jwt.DecodeError:
            return jsonify({
                        'error': 'Token invalide ',
                        'message': 'erreur lors du décodage du token'
                    }), 403
        except jwt.InvalidTokenError as error:
            return jsonify({
                'error': 'Token invalide',
                'message': str(error),
            }), 403
        except Exception as error:
            print(error)
            return jsonify({
                'error': 'Erreur inattendue',
                'message': str(error)
            }), 500
