import pytest
import os
from dotenv import load_dotenv
from src.main import create_app
from src.models.user import User
import uuid

from src.redis_client import get_redis_client, reset_redis_client
from src.utils import hash_password

load_dotenv(override=False)

EMAIL_KEY = os.getenv('EMAIL_KEY')
USER_KEY = os.getenv('USER_KEY')


@pytest.fixture(scope='session', autouse=True)
def setup_test_environment():
    """
    Configure l'environnement de test avant tous les tests.
    autouse =True : s'exécute automatiquement.
    scope ='session' : une seule fois pour toute la session de tests.
    """
    os.environ['FLASK_TESTING'] = 'true'
    reset_redis_client()
    yield
    os.environ['FLASK_TESTING'] = 'false'
    reset_redis_client()



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
    """ Client Redis de test pour la base de donnees de tests (db 1)"""
    redis_client = get_redis_client()

    # Verification de la base de donnees.
    current_db = redis_client.connection_pool.connection_kwargs.get('db')
    expected_db = int(os.getenv('REDIS_TEST_DB'))

    if current_db != expected_db:
        raise RuntimeError(
            f"ERREUR: Redis connecté à DB {current_db} au lieu de DB {expected_db} (test)!\n"
            f"FLASK_TESTING={os.getenv('FLASK_TESTING')}"
        )
    # Nettoyage de la BD avant le test
    redis_client.flushdb()
    # Execution du test
    yield redis_client
    # Nettoyage de la BD après le test
    redis_client.flushdb()



@pytest.fixture
def test_user(redis_client):
    """
        Ce fixture permet de créer un utilisateur de role USER de test dans la base de donnees directement.
        Il procède directement sans passer par la route /register.
    """
    email = "test10@mail.com"
    password = "Password123!"
    user_id = str(uuid.uuid4())

    user = User(
        id_user=user_id,
        firstname="Test",
        lastname="User",
        email=email,
        role="USER",
        token="",
        password=hash_password(password),
    )

    # enregistrement de l'utilisateur selon notre logique du registration
    redis_client.set(name=f"{EMAIL_KEY}{email}", value=f"{user.id_user}")
    redis_client.set(name=f"{USER_KEY}{user.id_user}", value=user.to_redis())

    # retour de l'utilisateur enregistré
    return {
        'user': user,
        'user_id': user.id_user,
        'email': email,
        'password': password,
        'role': 'USER'
    }