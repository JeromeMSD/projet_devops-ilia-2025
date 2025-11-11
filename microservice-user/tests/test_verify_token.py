import os
from datetime import timedelta
from src.models.user import User

from src.utils import create_token

USER_KEY = os.getenv('USER_KEY')
BASE_API_URL = os.getenv('BASE_API_URL')


class TestVerifyToken:
    """Tests pour la route /verify-token"""

    def test_verify_token_success(self, client, test_user, redis_client):
        """Test : Vérification d'un token valide"""

        # Connexion et obtention d'un token
        login_body: dict = {
            'email': test_user['email'],
            'password': test_user['password'],
        }
        login_response = client.post(f'{BASE_API_URL}/login', json=login_body)
        token = login_response.get_json()['user']['token']
        # Vérification du token
        response = client.get(f'{BASE_API_URL}/verify-token', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
        assert data['message'] == 'Utilisateur connecté'
        assert 'user' in data
        assert data['user']['email'] == test_user['email']

    def test_verify_token_missing_token(self, client):
        """Test : Requête sans token"""
        response = client.get(f'{BASE_API_URL}/verify-token')
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data

    def test_verify_token_invalid_token(self, client):
        """ Test : Token JWT invalide"""
        invalid_token: str = 'invalid_token_abcdefgh'
        response = client.get(f'{BASE_API_URL}/verify-token', headers={'Authorization': f'Bearer {invalid_token}'})
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert 'invalide' in data['error'].lower()

    def test_verify_token_revoked(self, client, test_user, redis_client):
        """ Test : Token révoqué"""
        # Se connecter
        login_body: dict = {
            'email': test_user['email'],
            'password': test_user['password'],
        }
        login_response = client.post(f'{BASE_API_URL}/login', json=login_body)
        token = login_response.get_json()['user']['token']
        # Révoquer le token (le vider dans Redis)
        user = User.from_redis_to_user(redis_client.get(name=f"{USER_KEY}{test_user['user_id']}"))
        user.token = ""
        redis_client.set(name=f"{USER_KEY}{test_user['user_id']}", value=user.to_redis())
        # Vérifier le token
        response = client.get(f'{BASE_API_URL}/verify-token', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert 'révoqué' in data['error'].lower() or 'expiré' in data['error'].lower()

    def test_verify_token_different_token(self, client, test_user, redis_client):
        """Test : Token valide, mais différent de celui stocké"""
        # Connection d'un utilisateur de tests
        login_body: dict = {
            'email': test_user['email'],
            'password': test_user['password'],
        }
        client.post(f'{BASE_API_URL}/login', json=login_body)
        # Creation d'un autre token valide
        another_token = create_token(test_user['user_id'])
        # Vérifier avec l'autre token
        response = client.get(f'{BASE_API_URL}/verify-token', headers={'Authorization': f'Bearer {another_token}'})
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert 'invalide' in data['error'].lower()

    def test_verify_token_expired(self, client, test_user, redis_client, monkeypatch):
        """Test : Token expiré"""
        # Login de l'utilisateur de test avec un token valide
        login_body: dict = {
            'email': test_user['email'],
            'password': test_user['password'],
        }
        client.post(f'{BASE_API_URL}/login', json=login_body)
        expired_token: str = create_token(user_id=test_user['user_id'], validity=-timedelta(seconds=1))
        # Vérification du token expire
        response = client.get(f'{BASE_API_URL}/verify-token', headers={'Authorization': f'Bearer {expired_token}'})
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert 'expiré' in data['error'].lower()
        # Vérification du nettoyage du token dans Redis
        user = User.from_redis_to_user(redis_client.get(f"{USER_KEY}{test_user['user_id']}"))
        assert user.token == ""
