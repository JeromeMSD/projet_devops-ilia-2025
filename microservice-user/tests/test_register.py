import pytest


class TestRegister:
    """Tests pour la route /register"""
    API_URL = '/api/v1/register'

    @pytest.fixture
    def base_user_data(self, redis_client):
        """Données utilisateur valides de base"""
        return {
            'firstname': 'Devops',
            'lastname': 'Testeur',
            'email': 'devops.testeur@example.com',
            'password': 'Password123',
            'role': 'USER'
        }

    def test_register_success(self, client, base_user_data):
        """Test : Création d'utilisateur réussie"""
        response = client.post(self.API_URL, json=base_user_data)
        assert response.status_code == 201
        data = response.get_json()
        assert 'message' in data
        assert 'user' in data
        assert data['user']['email'] == base_user_data['email'].lower()
        assert data['user']['firstname'] == base_user_data['firstname']
        assert data['user']['lastname'] == base_user_data['lastname']
        assert data['user']['role'] == base_user_data['role']
        assert 'password' not in data['user']

    def test_register_missing_body(self, client):
        """Test : Requête sans body"""
        response = client.post(self.API_URL, json=None)
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    @pytest.mark.parametrize("missing_field", [
        'firstname',
        'lastname',
        'email',
        'password',
        'role'
    ])
    def test_register_missing_fields(self, client, base_user_data, missing_field):
        """Test : Champs manquants"""
        invalid_data = base_user_data.copy()
        del invalid_data[missing_field]
        response = client.post(self.API_URL, json=invalid_data)
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert missing_field in data['error']

    @pytest.mark.parametrize("invalid_email", [
        'invalid-email',  # Pas de @
        'test@',  # Pas de domaine
        '@example.com',  # Pas de partie locale
        'test@example',  # Pas d'extension
        'test @example.com',  # Espace
    ])
    def test_register_invalid_email(self, client, base_user_data, invalid_email):
        """Test : Emails invalides"""
        invalid_data = base_user_data.copy()
        invalid_data['email'] = invalid_email
        response = client.post(self.API_URL, json=invalid_data)
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'email' in data['error'].lower()

    @pytest.mark.parametrize("invalid_password, reason", [
        ('court', 'Moins de 6 caractères'),
        ('sanschiffre', 'Pas de chiffre'),
        ('sansmajuscule1', 'Pas de majuscule'),
        ('Abc12', 'Trop court (5 chars)'),
    ])
    def test_register_invalid_password(self, client, base_user_data, invalid_password, reason):
        """Test : Mots de passe invalides"""
        invalid_data = base_user_data.copy()
        invalid_data['password'] = invalid_password
        response = client.post(self.API_URL, json=invalid_data)
        assert response.status_code == 400, f"Failed for password '{invalid_password}' ({reason})"
        data = response.get_json()
        assert 'error' in data
        assert 'password' in data['error'].lower()

    @pytest.mark.parametrize("invalid_role", [
        'GUEST',
        'SUPERADMIN',
        '',
        'qwerty'
    ])
    def test_register_invalid_role(self, client, base_user_data, invalid_role):
        """Test : Rôles invalides"""
        invalid_data = base_user_data.copy()
        invalid_data['role'] = invalid_role
        response = client.post(self.API_URL, json=invalid_data)
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'role' in data['error'].lower()

    def test_register_duplicate_email(self, client, base_user_data):
        """Test : Email déjà utilisé"""
        # Créer un premier utilisateur
        response1 = client.post(self.API_URL, json=base_user_data)
        assert response1.status_code == 201
        # Essayer de créer un deuxième utilisateur avec le même email
        response2 = client.post(self.API_URL, json=base_user_data)
        assert response2.status_code == 409
        data = response2.get_json()
        assert 'error' in data
        assert 'existe déjà' in data['error']

    def test_register_email_case_insensitive(self, client, base_user_data):
        """Test : Email en majuscules doit être converti en minuscules"""
        uppercase_data = base_user_data.copy()
        uppercase_data['email'] = 'JOHN.DOE@EXAMPLE.COM'
        response = client.post(self.API_URL, json=uppercase_data)
        assert response.status_code == 201
        data = response.get_json()
        assert data['user']['email'] == 'john.doe@example.com'
