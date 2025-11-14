from flask import Blueprint, request, jsonify, Response
from flask_cors import cross_origin
import os
import uuid
import re



from ..models.user import User
from src.redis_client import get_redis_client
from  dotenv import load_dotenv

from ..utils import hash_password

load_dotenv()

EMAIL_KEY = os.getenv('EMAIL_KEY')
USER_KEY = os.getenv('USER_KEY')


register_bp=Blueprint('register',__name__)



@register_bp.route('/register', methods=['POST'])
@cross_origin()
def register_user() -> tuple[Response, int]:
    # Extraction du body
    data: dict = request.get_json(silent=True)

    if data is None:
        return jsonify({
            'error': 'Corps de la requête vide ou invalide'
        }), 400

    # Vérification des champs requis
    required_fields = ['firstname', 'lastname', 'email', 'password', 'role']
    errors = {}
    for field in required_fields:
        if field not in data or not data[field]:
            errors[field] = f'{field} est requis'
    if errors:
        return jsonify({'error': str(errors)}), 400

    # verification du mot de passe par une regex validant les emails
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{3}$"
    if not re.fullmatch(email_regex, data['email']):
        errors['email'] = 'Veuillez entrer un email valide'

    # verification du mot de passe par une regex validant un mot de passe d'au moins six caractères
    # contenant au moins une majuscule, au moins un chiffre.
    password_regex = r"^(?=.*[A-Z])(?=.*\d).{6,}$"
    if not re.search(password_regex, data['password']):
        errors['password'] = 'Le mot de passe doit contenir au moins 6 caractères, une majuscule et un chiffre'


    if str(data['role']).upper() not in ['USER', 'ADMIN', 'SRE']:
        errors['role'] = 'Le rôle doit être USER,  ADMIN ou un SRE'


    if errors:
        return jsonify({'error': str(errors)}), 400

    try:
        email = data['email'].lower().strip()
        user_key_email = f'{EMAIL_KEY}{email}'
        redis_client = get_redis_client()

        if redis_client.exists(user_key_email):
            return jsonify({'error': 'Un utilisateur avec cet email existe déjà.'}), 409

        hashed_password = hash_password(data['password'])
        id_user = str(uuid.uuid4())
        user = User(
            id_user=id_user,
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=email,
            token="",
            role=data['role'],
            password=hashed_password,
        )
        redis_client.set(name=user_key_email, value=user.id_user)
        redis_client.set(name=f"{USER_KEY}{user.id_user}", value=user.to_redis())

        return jsonify({
            'message': 'Utilisateur créé avec succès.',
            'user': user.to_json()
        }), 201

    except Exception as error:
        print(f"Erreur lors de l'enregistrement: {error}")
        return jsonify({
            'message': 'Erreur interne lors de la création de l\'utilisateur, veuillez réessayer plus tard',
            'error': str(error)
        }), 500