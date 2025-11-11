"""
Test suite for Find Users endpoint (with optional role filtering)
Run with: pytest tests/test_find_users_by_role.py -v
"""
import os
import pytest

BASE_API_URL = os.getenv('BASE_API_URL')

# Fixtures


@pytest.fixture
def sample_admin_user():
    """Sample admin user data for testing"""
    return {
        "firstname": "Admin",
        "lastname": "Testeur",
        "email": "admin@example.com",
        "password": "Password123",
        "role": "ADMIN"
    }


@pytest.fixture
def get_admin_token(client, sample_admin_user, redis_client):
    """Create and login a sample admin user"""
    # Create admin user first
    create_response = client.post(f'{BASE_API_URL}/register', json=sample_admin_user)
    assert create_response.status_code == 201
    # Login the created admin user
    login_response = client.post(f'{BASE_API_URL}/login', json={
        "email": sample_admin_user["email"],
        "password": sample_admin_user["password"]
    })
    assert login_response.status_code == 200
    user = login_response.get_json()['user']
    return user


@pytest.fixture
def get_user_token(client, redis_client):
    """Create and login a regular USER for permission testing"""
    user_data = {
        "firstname": "Regular",
        "lastname": "User",
        "email": "regular@example.com",
        "password": "Password123",
        "role": "USER"
    }
    # Create user
    create_response = client.post(f'{BASE_API_URL}/register', json=user_data)
    assert create_response.status_code == 201
    # Login user
    login_response = client.post(f'{BASE_API_URL}/login', json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    assert login_response.status_code == 200
    user = login_response.get_json()['user']
    return user


@pytest.fixture
def get_sre_token(client, redis_client):
    """Create and login a SRE user"""
    sre_data = {
        "firstname": "SRE",
        "lastname": "Engineer",
        "email": "sre@example.com",
        "password": "Password123",
        "role": "SRE"
    }
    # Create SRE
    create_response = client.post(f'{BASE_API_URL}/register', json=sre_data)
    assert create_response.status_code == 201
    # Login SRE
    login_response = client.post(f'{BASE_API_URL}/login', json={
        "email": sre_data["email"],
        "password": sre_data["password"]
    })

    assert login_response.status_code == 200
    user = login_response.get_json()['user']
    return user


class TestFindUsers:
    """Test find users endpoint (with optional role filtering)"""
    # ========== Tests sans filtrage (tous les utilisateurs) ==========
    def test_get_all_users_without_filter(self, client, redis_client, get_admin_token):
        """
        Test: Récupérer tous les utilisateurs sans filtrage
        - Appel GET /users (sans query param)
        - Doit retourner TOUS les utilisateurs
        - Doit retourner 200
        """
        # Arrange: Créer plusieurs utilisateurs avec différents rôles
        users_data = [
            {"firstname": "Admin1", "lastname": "Test", "email": "admin1@test.com", "password": "Password123", "role": "ADMIN"},
            {"firstname": "User1", "lastname": "Test", "email": "user1@test.com", "password": "Password123", "role": "USER"},
            {"firstname": "SRE1", "lastname": "Test", "email": "sre1@test.com", "password": "Password123", "role": "SRE"}
        ]
        for user_data in users_data:
            response = client.post(f'{BASE_API_URL}/register', json=user_data)
            assert response.status_code == 201
        # Act: Appeler /users SANS query param
        response = client.get(
            f'{BASE_API_URL}/users',
            headers={'Authorization': f'Bearer {get_admin_token["token"]}'}
        )
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert 'count' in data
        assert 'users' in data
        assert data['count'] >= 4  # Au moins les 3 créés + l'admin du fixture

    def test_get_all_users_only_admin_in_db(self, client, redis_client, get_admin_token):
        """
        Test: Récupérer tous les utilisateurs quand seul l'admin existe
        - La base de données ne contient que l'admin du fixture
        - Doit retourner 200 avec count = 1
        """
        # Act
        response = client.get(
            f'{BASE_API_URL}/users',
            headers={'Authorization': f'Bearer {get_admin_token["token"]}'}
        )
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 1
        assert data['users'] == [get_admin_token]

    def test_users_attributes_not_empty(self, client, redis_client, get_admin_token):
        """
        Test: Vérifier que tous les attributs des utilisateurs sont présents et non vides
        - Vérifie: firstname, lastname, email, role, id_user, token, created_at
        - Password ne doit PAS être dans la réponse
        """
        # Act: Récupérer tous les utilisateurs
        response = client.get(
            f'{BASE_API_URL}/users',
            headers={'Authorization': f'Bearer {get_admin_token["token"]}'}
        )
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert 'users' in data
        assert len(data['users']) > 0
        # Vérifier chaque utilisateur
        for user in data['users']:
            assert 'firstname' in user
            assert user['firstname'] is not None
            assert user['firstname'] != ""
            assert 'lastname' in user
            assert user['lastname'] is not None
            assert user['lastname'] != ""
            assert 'email' in user
            assert user['email'] is not None
            assert user['email'] != ""
            assert 'role' in user
            assert user['role'] is not None
            assert user['role'] != ""
            assert 'id_user' in user
            assert user['id_user'] is not None
            assert user['id_user'] != ""
            assert 'token' in user
            assert 'created_at' in user
            assert user['created_at'] is not None
            assert user['created_at'] != ""
            # Password ne doit PAS être présent
            assert 'password' not in user
    # ========== Tests avec filtrage par rôle ==========

    def test_get_users_by_role_admin(self, client, redis_client, get_admin_token):
        """
        Test: Filtrer les utilisateurs par rôle ADMIN
        - Appel GET /users?role=ADMIN
        - Doit retourner seulement les ADMIN
        - Doit retourner 200
        """
        # Arrange: Créer plusieurs utilisateurs avec différents rôles
        users_data = [
            {"firstname": "Admin1", "lastname": "Test", "email": "admin1@test.com", "password": "Password123", "role": "ADMIN"},
            {"firstname": "User1", "lastname": "Test", "email": "user1@test.com", "password": "Password123", "role": "USER"},
            {"firstname": "Admin2", "lastname": "Test", "email": "admin2@test.com", "password": "Password123", "role": "ADMIN"},
            {"firstname": "SRE1", "lastname": "Test", "email": "sre1@test.com", "password": "Password123", "role": "SRE"}
        ]
        for user_data in users_data:
            response = client.post(f'{BASE_API_URL}/register', json=user_data)
            assert response.status_code == 201
        # Act: Filtrer par rôle ADMIN
        response = client.get(
            f'{BASE_API_URL}/users?role=ADMIN',
            headers={'Authorization': f'Bearer {get_admin_token["token"]}'}
        )
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 3  # Admin1 + Admin2 + admin du fixture
        for user in data['users']:
            assert user['role'] == 'ADMIN'

    def test_get_users_by_role_user(self, client, redis_client, get_admin_token):
        """
        Test: Filtrer les utilisateurs par rôle USER
        - Appel GET /users?role=USER
        - Doit retourner seulement les USER
        - Doit retourner 200
        """
        # Arrange
        users_data = [
            {"firstname": "User1", "lastname": "Test", "email": "user1@test.com", "password": "Password123", "role": "USER"},
            {"firstname": "User2", "lastname": "Test", "email": "user2@test.com", "password": "Password123", "role": "USER"},
            {"firstname": "Admin1", "lastname": "Test", "email": "admin1@test.com", "password": "Password123", "role": "ADMIN"}
        ]
        for user_data in users_data:
            response = client.post(f'{BASE_API_URL}/register', json=user_data)
            assert response.status_code == 201
        # Act
        response = client.get(
            f'{BASE_API_URL}/users?role=USER',
            headers={'Authorization': f'Bearer {get_admin_token["token"]}'}
        )
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 2  # User1 + User2
        for user in data['users']:
            assert user['role'] == 'USER'

    def test_get_users_by_role_sre(self, client, redis_client, get_admin_token):
        """
        Test: Filtrer les utilisateurs par rôle SRE
        - Appel GET /users?role=SRE
        - Doit retourner seulement les SRE
        - Doit retourner 200
        """
        # Arrange
        sre_user = {"firstname": "SRE", "lastname": "Engineer", "email": "sre@test.com", "password": "Password123", "role": "SRE"}
        response = client.post(f'{BASE_API_URL}/register', json=sre_user)
        assert response.status_code == 201
        # Act
        response = client.get(
            f'{BASE_API_URL}/users?role=SRE',
            headers={'Authorization': f'Bearer {get_admin_token["token"]}'}
        )
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 1
        assert data['users'][0]['role'] == 'SRE'
        assert data['users'][0]['email'] == 'sre@test.com'

    def test_get_users_by_role_empty_result(self, client, redis_client, get_admin_token):
        """
        Test: Filtrer avec un rôle inexistant
        - Appel GET /users?role=INEXISTANT
        - Doit retourner une liste vide
        - Doit retourner 200
        """
        # Act
        response = client.get(
            f'{BASE_API_URL}/users?role=INEXISTANT',
            headers={'Authorization': f'Bearer {get_admin_token["token"]}'}
        )
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 0
        assert data['users'] == []

    def test_get_users_by_role_case_insensitive(self, client, redis_client, get_admin_token):
        """
        Test: Le filtre de rôle est insensible à la casse
        - 'admin', 'ADMIN', 'Admin' devraient tous fonctionner
        - Doit retourner 200 avec les mêmes résultats
        """
        # Arrange
        admin_user = {"firstname": "Admin", "lastname": "Test", "email": "admin@test.com", "password": "Password123", "role": "ADMIN"}
        client.post(f'{BASE_API_URL}/register', json=admin_user)
        # Act: Tester différentes casses
        for role_variant in ['admin', 'ADMIN', 'Admin']:
            response = client.get(
                f'{BASE_API_URL}/users?role={role_variant}',
                headers={'Authorization': f'Bearer {get_admin_token["token"]}'}
            )
            # Assert
            assert response.status_code == 200
            data = response.get_json()
            assert data['count'] >= 2  # Au moins l'admin fixture + l'admin créé

    # ========== Tests de sécurité et permissions ==========
    def test_get_users_unauthorized(self, client):
        """
        Test: Accès sans token d'authentification
        - Doit retourner 403
        """
        # Act
        response = client.get(f'{BASE_API_URL}/users')
        # Assert
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data

    def test_get_users_insufficient_permissions(self, client, get_user_token):
        """
        Test: Accès avec un token USER (permissions insuffisantes)
        - Seuls ADMIN et SRE peuvent accéder
        - Doit retourner 403
        """
        # Act
        response = client.get(
            f'{BASE_API_URL}/users',
            headers={'Authorization': f'Bearer {get_user_token["token"]}'}
        )
        # Assert
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert 'permission' in data['error'].lower()

    def test_get_users_sre_has_permission(self, client, get_sre_token):
        """
        Test: SRE a les permissions pour accéder à /users
        - Doit retourner 200
        """
        # Act
        response = client.get(
            f'{BASE_API_URL}/users',
            headers={'Authorization': f'Bearer {get_sre_token["token"]}'}
        )
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert 'count' in data
        assert 'users' in data
