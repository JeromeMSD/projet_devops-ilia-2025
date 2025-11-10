from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import redis
import time
from models.user import User
from utils import hash_password, create_token
from redis_client import get_redis_client


Create_user = Blueprint('createUser', __name__)


@Create_user.route('/api/v1/users', methods=['POST'])
@cross_origin()
def create_user():
    """
    Route pour créer un nouvel utilisateur et le stocker dans Redis.

    Expected JSON body:
        {
            "firstname": "John",
            "lastname": "Doe",
            "email": "john@example.com",
            "password": "securePassword123"
        }

    Returns:
        JSON: L'utilisateur créé avec son token

    Responses:
        201: Utilisateur créé avec succès
        400: Données manquantes ou invalides
        409: Email déjà existant
        500: Erreur serveur
    """
    try:
        # Obtenir le client Redis
        redis_client = get_redis_client()

        # Vérifier la connexion Redis
        if redis_client is None:
            return jsonify({
                "error": "Database connection unavailable"
            }), 500

        # Récupérer les données du body
        data = request.get_json()

        # Validation des champs requis
        required_fields = ['firstname', 'lastname', 'email', 'password']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify({
                "error": "Missing required fields",
                "missing": missing_fields
            }), 400

        firstname = data.get('firstname')
        lastname = data.get('lastname')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')  # Default role is 'user'

        # Validation basique
        if not email or '@' not in email:
            return jsonify({
                "error": "Invalid email format"
            }), 400

        if not password or len(password) < 6:
            return jsonify({
                "error": "Password must be at least 6 characters long"
            }), 400

        # Vérifier si l'email existe déjà
        # On parcourt toutes les clés user:* pour vérifier l'email
        user_keys = redis_client.keys('user:*')
        for key in user_keys:
            user_data = redis_client.get(key)
            if user_data:
                existing_user = User.from_redis_to_user(user_data)
                if existing_user.email == email:
                    return jsonify({
                        "error": "Email already exists"
                    }), 409

        # Générer un ID utilisateur unique basé sur timestamp
        user_id = f"USR-{int(time.time())}"

        # Hasher le mot de passe
        hashed_pwd = hash_password(password)

        # Créer le token JWT
        token = create_token(user_id)

        # Créer l'objet User
        new_user = User(
            id_user=user_id,
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=hashed_pwd,
            role=role,
            token=token
        )

        # Sauvegarder dans Redis
        redis_key = f"user:{user_id}"
        redis_client.set(redis_key, new_user.to_redis())

        # Retourner l'utilisateur créé (sans le password)
        return jsonify({
            "message": "User created successfully",
            "user": new_user.to_json()
        }), 201

    except redis.ConnectionError:
        return jsonify({
            "error": "Cannot connect to database"
        }), 500

    except Exception as e:
        print(f"Erreur inattendue dans create_user: {e}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500
