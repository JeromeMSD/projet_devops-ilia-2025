import pytest
import json
from src.utils import verify_token


class TestLogin:
    """Tests pour la route /login"""

    def test_login_success(self,   client, test_user):
        """Test : Connexion réussie avec credentials valides"""
        response = client.post('/login',
                               json={
                                   'email': test_user['email'],
                                   'password': test_user['password']
                               },
                               content_type='application/json'
                               )

        assert response.status_code == 200
        data = response.get_json()

        # Vérifier la structure de la réponse
        assert 'user' in data
        assert 'message' in data
        assert data['message'] == 'Successfully logged in!'

        # Vérifier les infos utilisateur
        assert data['user']['email'] == test_user['email']
        assert data['user']['firstname'] == 'Test'
        assert 'token' in data['user']
        assert data['user']['token'] != ""

        # Vérifier que le token est valide
        token = data['user']['token']
        payload = verify_token(token)
        assert payload is not None
        assert payload['id_user'] == test_user['user_id']


    def test_login_wrong_password(self, client, test_user):
        """Test : Connexion avec mot de passe incorrect"""
        response = client.post('/login',
                               json={
                                   'email': test_user['email'],
                                   'password': 'WrongPassword123!'
                               },
                               content_type='application/json'
                               )

        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Mot de passe incorrect'

    def test_login_user_not_found(self, client):
        """Test : Connexion avec email inexistant"""
        response = client.post('/login',
                               json={
                                   'email': 'nonexistent@mail.com',
                                   'password': 'Password123!'
                               },
                               content_type='application/json'
                               )

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Utilisateur inexistant'

    def test_login_missing_email(self, client):
        """Test : Requête sans email"""
        response = client.post('/login',
                               json={'password': 'Password123!'},
                               content_type='application/json'
                               )

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'email' in data['error'].lower()

    def test_login_missing_password(self, client, test_user):
        """Test : Requête sans password"""
        response = client.post('/login',
                               json={'email': test_user['email']},
                               content_type='application/json'
                               )

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'password' in data['error'].lower()

    def test_login_empty_body(self, client):
        """Test : Requête avec body vide"""
        response = client.post('/login',
                               data='',
                               content_type='application/json'
                               )

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_login_invalid_json(self, client):
        """Test : Requête avec JSON invalide"""
        response = client.post('/login',
                               data='invalid json',
                               content_type='application/json'
                               )

        assert response.status_code == 400



    def test_login_token_stored_in_redis(self, client, test_user, redis_client):
        """Test : Vérifier que le token est stocké dans Redis"""
        response = client.post('/login',
                               json={
                                   'email': test_user['email'],
                                   'password': test_user['password']
                               },
                               content_type='application/json'
                               )

        assert response.status_code == 200
        data = response.get_json()
        token = data['user']['token']

        # Récupérer l'utilisateur depuis Redis
        user_bytes = redis_client.get(test_user['user_id'])
        assert user_bytes is not None

        # Vérifier que le token est bien stocké
        from src.models.user import User
        user = User.from_redis_to_user(user_bytes)
        assert user.token == token