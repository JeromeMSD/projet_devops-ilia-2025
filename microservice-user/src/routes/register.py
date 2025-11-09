from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import os
import uuid
import bcrypt
import re

from ..models.user import User
from src.redis_client import get_redis_client
from  dotenv import load_dotenv

load_dotenv()

EMAIL_KEY = os.getenv('EMAIL_KEY')
USER_KEY = os.getenv('USER_KEY')


register_bp=Blueprint('register',__name__)




@register_bp.route('/register', methods=['POST'])
@cross_origin()
def register_user():

    # extraction du body de la requete
    data: dict = request.get_json(silent=True)

    requested_keys: list = ['firstname', 'lastname', 'email', 'password', 'role']
    if data is None:
        return jsonify({
            'error': 'Les champs email, password, et firstname , lastname, et role sont requis.'
            }), 400
    
    missing_fields = {}
    for key in requested_keys:
        if key not in data.keys():
            missing_fields[key] = f'{key} manquant'
        elif key == 'password' and data['password']:
            password_regex = r"^(?=.*[A-Z])(?=.*\d).{6,}$"
            if not re.search(password_regex, data['password']):
                 missing_fields[key] = 'Veuillez entrer un mot de passe valide'
        elif key == 'email' and data['email']:
            email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.fullmatch(email_regex, data['email']):
                missing_fields[key] = 'Veuillez entrer un email valide'
        elif key == 'role' and data['role']:
            if data['role'] not in ['USER', 'ADMIN']:
                missing_fields[key] = 'entrer un role valide entre ' + ['USER', 'ADMIN']
            print(data['role'])


    if missing_fields:
        return jsonify({
            'error': f"{missing_fields}"
            }), 400


    email = data['email'].lower().strip()
    password = data['password']
    user_key_email = f'{EMAIL_KEY}{email}'

    redis_client = get_redis_client()
    
    if redis_client.exists(user_key_email):
        return jsonify({'error': 'Un utilisateur avec cet email existe déjà.'}), 409

 
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
            redis_client.set(name=user_key_email, value = f"{user.id_user}")
            redis_client.set(name=f"{USER_KEY}{user.id_user}", value = user.to_redis())
            return jsonify({
                'message': 'Utilisateur créé avec succès.',
                'user': user.to_json(),
            }), 201
        except Exception as error:
            print(f"Erreur lors de l'enregistrement de l'utilisateur: {error}")
            return jsonify({'error': str(error)}), 500

    except Exception as error:
        print(f"Erreur lors de l'enregistremen de l'utilisateurt: {error}")
        return jsonify({
            'message': "Erreur interne lors de la création de l'utilisateur.",
            'error': str(error)
        }), 500
