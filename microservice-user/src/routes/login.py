import os
import uuid
from dotenv import load_dotenv

load_dotenv()

import bcrypt
import jwt
from flask import Blueprint, request, jsonify
import redis
from ..utils import verify_password, create_token, verify_token
from ..models.user import User


login_bp = Blueprint('login', __name__)
EMAIL_KEY = os.getenv('EMAIL_KEY')


redis_client = redis.Redis(
    host= os.getenv('REDIS_HOST'),
    port= int(os.getenv('REDIS_PORT')),
    db=0
)





@login_bp.route('/login', methods=['POST'])
def login_route():
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
    try:
        # extraction du 'body' de la requête HTTP
        data = request.get_json(silent=True)
        if not data:
            return jsonify({
                'error': 'Les champs email et mots de password sont requis'
            }), 400
        elif not data.get('email') :
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
            user_id_bytes  = redis_client.get(f"{EMAIL_KEY}{email}")

            if not user_id_bytes:
                return jsonify({
                    'error': 'Utilisateur inexistant'
                }), 404

            else:
                user_id: str = user_id_bytes.decode("utf-8") if isinstance(user_id_bytes, bytes) else user_id_bytes
                redis_object : bytes = redis_client.get(user_id)
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
                    redis_client.set(name = user_id, value = user_infos.to_redis())

                    # Retour d'une réponse HTTP 200 avec les infos de l'utilisateur
                    return jsonify({
                        'user': user_infos.to_json(),
                        'message': 'Successfully logged in!'
                    }), 200
    except Exception as error:
        print(f"error", error)
        return jsonify({
            'message': "Une erreur inattendue est survenue, veuillez réessayer plus tard !",
            'error': str(error)
        }), 500





@login_bp.route('/verify-token', methods=['GET'])
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
                - 500 500 Internal Server Error: Erreur d'exécution inattendue.
    """

    # Recuperation du champ Authorization dans les headers de la requête.
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        # Verification du token
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Token JWT invalide'}), 403
        else:
            # Token valide
            if type(payload) == dict:
                user_id = payload['id_user']
                user_role = payload['role']
                user: User = User.from_redis_to_user(redis_client.get(user_id))
                stored_token = user.token

                # Verification de l'intégrité du token
                if not stored_token or stored_token=="":
                    return jsonify({'error': 'Token révoqué ou expiré, veuillez vous reconnecter !'}), 403

                elif stored_token != token:
                    return jsonify({'error': 'Token invalide'}), 403



                else:
                    return jsonify(
                        {
                            'message': "Utilisateur connecté",
                            'user': user.to_json(),
                        }
                    ), 200

            # Token expiree
            elif type(payload) == str:
                user_id = payload
                user = User.from_redis_to_user(redis_client.get(user_id))
                user.token = ""
                redis_client.set(name = user_id, value = user.to_redis())
                return jsonify({
                    'error': 'Token expiré, veuillez vous reconnecter'
                }), 403
            else:
                return jsonify({'error': 'Erreur inattendue'}), 500

     # Gestion des erreurs
    except jwt.DecodeError as error:
        return jsonify({
                    'error': f'Token invalide - {error}'
                }), 403
    except jwt.InvalidTokenError:
        return jsonify({
            'error': 'Token invalide'
        }), 403
    except Exception as error:
        print(error)
        return jsonify({
            'error': 'Erreur inattendue'
        }), 500






@login_bp.route('/register', methods=['POST'])
def register_route():
    data = request.get_json(silent=True)
    if data is None or 'email' not in data or 'password' not in data or 'role' not in data or 'firstname' not in data or 'lastname' not in data:
        return jsonify({'error': 'Les champs email, password, et first_name , lastname, role sont requis.'}), 400
    email = data['email'].lower().strip()
    password = data['password']
    user_key = f'{EMAIL_KEY}{email}'
    if redis_client.exists(user_key):
        return jsonify({'error': 'Un utilisateur avec cet email existe déjà.'}), 409

    if not str(data['role']).__eq__("USER") or not str(data['role']).__eq__("ADMIN") or not str(data['role']).__eq__("TECHNICIEN"):
        return jsonify({
            'error': 'Le champ role doit être soit un user, soit un admin soit un technicien'
        }), 400
    try:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        id_user = str(uuid.uuid4())
        user: User = User(
            id_user=id_user,
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=email,
            token="",
            role=data['role'],
            password=hashed_password.decode('utf-8'),
        )
        try :
            redis_client.set(name=user_key, value = user.id_user)
            redis_client.set(name=id_user, value = user.to_redis())
            return jsonify({
                'message': 'Utilisateur créé avec succès.',
                'user': user.to_json(),
            }), 201
        except Exception as e:
            print(f"Erreur lors de l'enregistrement: {e}")
            return jsonify({'error': str(e)}), 500

    except Exception as e:
        print(f"Erreur lors de l'enregistrement: {e}")
        return jsonify({
            'message': "Erreur interne lors de la création de l'utilisateur.",
            'error': str(e)
        }), 500