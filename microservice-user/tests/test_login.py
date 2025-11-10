import os

from dotenv import load_dotenv

from src.utils import verify_token
load_dotenv()

BASE_API_URL = os.getenv('BASE_API_URL')

class TestLogin:
    """Tests pour la route /login"""

    def test_login_success(self,  client, test_user):
        """Test : Connexion réussie avec credentials valides"""

        login_body: dict = {
            'email': test_user['email'],
            'password': test_user['password'],
        }

        response = client.post(f'{BASE_API_URL}/login', json=login_body, content_type='application/json')

      #  print(f'{BASE_API_URL}/login')
      #  print(response.json())
        assert response.status_code == 200

        login_data: dict = response.get_json()

        # Vérification de la structure de la réponse
        assert 'user' in login_data
        assert 'message' in login_data

        # Vérifier les infos utilisateur
        assert login_data['user']['email'] == test_user['email']
        assert login_data['user']['firstname'] == 'Test'
        assert 'token' in login_data['user']
        assert login_data['user']['token'] != ""
        assert 'role' in login_data['user']
        assert login_data['user']['role'] == test_user['role']

        # Vérifier que le token est valide
        token = login_data['user']['token']
        payload = verify_token(token)
        assert payload is not None
        id_user: str = payload['id_user'].decode('utf-8') if isinstance(payload['id_user'], bytes) else str(payload['id_user'])
        assert id_user == test_user['user_id']




    def test_login_wrong_password(self, client, test_user):
        """Test : Connexion avec mot de passe incorrect"""

        wrong_login_body: dict= {
            'email': test_user['email'],
            'password': 'wrongPassword',

        }
        response = client.post(f'{BASE_API_URL}/login', json= wrong_login_body, content_type='application/json')

        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Mot de passe incorrect'




    def test_login_user_not_found(self, client):
        """Test : Connexion avec email inexistant"""

        wrong_login_body: dict = {
            'email': 'nonexistent@gmail.com',
            'password': 'password123',

        }
        response = client.post(f'{BASE_API_URL}/login', json=wrong_login_body, content_type='application/json')
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert data['error'] == 'Utilisateur inexistant'




    def test_login_missing_email(self, client):
        """Test : Requête sans email"""
        wrong_login_body: dict = {
            'password': 'password123',
        }
        response = client.post(f'{BASE_API_URL}/login', json= wrong_login_body, content_type='application/json')


        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'email' in data['error'].lower()




    def test_login_missing_password(self, client, test_user):
        """Test : Requête sans password"""

        wrong_login_body: dict = {
            'email': 'nonexistent@gmail.com',
        }
        response = client.post(f'{BASE_API_URL}/login', json=wrong_login_body, content_type='application/json')

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'password' in data['error'].lower()




    def test_login_empty_body(self, client):
        """Test : Requête avec body vide"""
        response = client.post(f'{BASE_API_URL}/login', json={}, content_type='application/json')

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data




    def test_login_invalid_json(self, client):
        """Test : Requête avec JSON invalide"""
        response = client.post(f'{BASE_API_URL}/login', data='invalid json', content_type='application/json')

        assert response.status_code == 400




