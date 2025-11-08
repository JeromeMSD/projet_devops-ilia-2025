# tests/conftest.py
import pytest
import redis
import os
from dotenv import load_dotenv
from src.main import create_app
from src.models.user import User
import bcrypt
import uuid

load_dotenv()


@pytest.fixture
def app():
    """Créer l'application Flask en mode test"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Client de test Flask"""
    return app.test_client()


@pytest.fixture
def redis_client():
    """Client Redis de test (DB 1 pour ne pas polluer la DB 0)"""
    r = redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6380)),
        db=0,  # ← CHANGER EN db=0 (même DB que l'app)
        decode_responses=False
    )

    # Nettoyer AVANT le test (au lieu d'après)
    # Seulement les clés de test
    test_keys = r.keys('email:test*') + r.keys('*test*')
    if test_keys:
        r.delete(*test_keys)

    yield r

    # Nettoyage après chaque test
    test_keys = r.keys('email:test*') + r.keys('*test*')
    if test_keys:
        r.delete(*test_keys)


@pytest.fixture
def test_user(redis_client):
    """Créer un utilisateur de test dans Redis"""
    email = "test@mail.com"
    password = "Password123!"
    user_id = str(uuid.uuid4())

    # Hasher le password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Créer l'utilisateur
    user = User(
        id_user=user_id,
        firstname="Test",
        lastname="User",
        email=email,
        role="USER",
        token="",
        password=hashed_password.decode('utf-8'),
    )

    # Stocker dans Redis (même structure que votre code)
    EMAIL_KEY = os.getenv('EMAIL_KEY')
    redis_client.set(name=f"{EMAIL_KEY}{email}", value = user_id.encode('utf-8'))  # ← Encoder en bytes
    redis_client.set(name = user_id.encode('utf-8'), value = user.to_redis().encode('utf-8'))  # ← Encoder en bytes

    return {
        'user': user,
        'user_id': user_id,
        'email': email,
        'password': password,
        'role': 'USER'
    }