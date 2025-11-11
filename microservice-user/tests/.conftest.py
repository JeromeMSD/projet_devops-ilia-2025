import pytest
import os
from dotenv import load_dotenv
from src.main import create_app
from src.models.user import User
import bcrypt
import uuid

from src.redis_client import get_redis_client

load_dotenv()

EMAIL_KEY = os.getenv('EMAIL_KEY')
USER_KEY = os.getenv('USER_KEY')




@pytest.fixture
def app():
    """Créer l'application Flask en mode test et active la DB de test."""

    os.environ['FLASK_TESTING'] = 'True'

    app = create_app()
    app.config['TESTING'] = True


    return app


@pytest.fixture
def client(app):
    """Client de test Flask"""
    return app.test_client()


# Dans tests/conftest.py

@pytest.fixture
def redis_client():
    redis_client = get_redis_client()

    #  Nettoyage de la BD avant le test

    #email_pattern = f"{EMAIL_KEY}test*".encode('utf-8')
    #user_pattern = f"{USER_KEY}test*".encode('utf-8')
    #test_keys = redis_client.keys(email_pattern) + redis_client.keys(user_pattern)

    

    #if test_keys:
        # Supprimer toutes les clés trouvées
    #    redis_client.delete(*test_keys)

    redis_client.flushdb

    yield redis_client

    redis_client.flushdb

    # Nettoyage de la BD apres le test.
    #test_keys = redis_client.keys(email_pattern) + redis_client.keys(user_pattern)
    #if test_keys:
    #    redis_client.delete(*test_keys)



@pytest.fixture
def test_user(redis_client):
    """Créer un utilisateur de test dans Redis"""
    email = "test10@mail.com"
    password = "Password123!"
    user_id = str(uuid.uuid4())


    # Hasher le password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Créer l'utilisateur
    user = User(
        id_user=f'test:{user_id}',
        firstname="Test",
        lastname="User",
        email=email,
        role="USER",
        token="",
        password=hashed_password.decode('utf-8'),
    )

    # Stocker dans Redis (même structure que votre code)

    redis_client.set(name=f"{EMAIL_KEY}{email}", value =f"{user.id_user}")
    redis_client.set(name =f"{USER_KEY}{user.id_user}", value = user.to_redis())

    return {
        'user': user,
        'user_id': user.id_user,
        'email': email,
        'password': password,
        'role': 'USER'
    }