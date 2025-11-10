"""
Test suite for Find Users by Role endpoint
Run with: pytest tests/test_find_users_by_role.py -v
"""
import os
import pytest

BASE_API_URL = os.getenv('BASE_API_URL')


class TestFindUsersByRole:
    """Test find users by role endpoint"""

    def test_get_users_by_role_admin_success(self, client, redis_client, get_admin_token):
        """
        Test: Récupérer avec succès les utilisateurs avec le rôle ADMIN
        - Doit retourner seulement les utilisateurs avec rôle ADMIN
        - Doit retourner 200
        """
        # Arrange: Créer plusieurs utilisateurs avec différents rôles
        users_data = [
            {"firstname": "Admin1", "lastname": "Test", "email": "admin1@test.com", "password": "Password123", "role": "ADMIN"},
            {"firstname": "User1", "lastname": "Test", "email": "user1@test.com", "password": "Password123", "role": "USER"},
            {"firstname": "Admin2", "lastname": "Test", "email": "admin2@test.com", "password": "Password123", "role": "ADMIN"},
            {"firstname": "SRE1", "lastname": "Test", "email": "sre1@test.com", "password": "Password123", "role": "SRE"}
        ]
        
        # Créer les utilisateurs
        for user_data in users_data:
            response = client.post(f'{BASE_API_URL}/register', json=user_data)
            assert response.status_code == 201

        # Act: Appeler la nouvelle route pour filtrer par rôle ADMIN
        response = client.get(
            f'{BASE_API_URL}/users/role/ADMIN',
            headers={'Authorization': f'Bearer {get_admin_token["token"]}'}
        )

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert 'count' in data
        assert 'users' in data
        assert data['count'] == 3  # Admin1 + Admin2 + l'admin du fixture get_admin_token
        for user in data['users']:
            assert user['role'] == 'ADMIN'

    def test_get_users_by_role_user_success(self, client, redis_client, get_admin_token):
        """
        Test: Récupérer avec succès les utilisateurs avec le rôle USER
        - Doit retourner seulement les utilisateurs avec rôle USER
        - Doit retourner 200
        """
        # Arrange: Créer plusieurs utilisateurs USER
        users_data = [
            {"firstname": "User1", "lastname": "Test", "email": "user1@test.com", "password": "Password123", "role": "USER"},
            {"firstname": "User2", "lastname": "Test", "email": "user2@test.com", "password": "Password123", "role": "USER"},
            {"firstname": "Admin1", "lastname": "Test", "email": "admin1@test.com", "password": "Password123", "role": "ADMIN"}
        ]
        
        for user_data in users_data:
            response = client.post(f'{BASE_API_URL}/register', json=user_data)
            assert response.status_code == 201

        # Act: Filtrer par rôle USER
        response = client.get(
            f'{BASE_API_URL}/users/role/USER',
            headers={'Authorization': f'Bearer {get_admin_token["token"]}'}
        )

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 2  # User1 + User2
        for user in data['users']:
            assert user['role'] == 'USER'

    def test_get_users_by_role_sre_success(self, client, redis_client, get_admin_token):
        """
        Test: Récupérer avec succès les utilisateurs avec le rôle SRE
        - Doit retourner seulement les utilisateurs avec rôle SRE
        - Doit retourner 200
        """
        # Arrange: Créer un utilisateur SRE
        sre_user = {"firstname": "SRE", "lastname": "Engineer", "email": "sre@test.com", "password": "Password123", "role": "SRE"}
        response = client.post(f'{BASE_API_URL}/register', json=sre_user)
        assert response.status_code == 201

        # Act: Filtrer par rôle SRE
        response = client.get(
            f'{BASE_API_URL}/users/role/SRE',
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
        Test: Récupérer les utilisateurs avec un rôle qui n'existe pas
        - Doit retourner une liste vide
        - Doit retourner 200
        """
        # Act: Filtrer par un rôle qui n'existe pas
        response = client.get(
            f'{BASE_API_URL}/users/role/INEXISTANT',
            headers={'Authorization': f'Bearer {get_admin_token["token"]}'}
        )

        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 0
        assert data['users'] == []

    def test_get_users_by_role_unauthorized(self, client):
        """
        Test: Accès sans token d'authentification
        - Doit retourner 403
        """
        # Act: Appeler sans token
        response = client.get(f'{BASE_API_URL}/users/role/ADMIN')

        # Assert
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data

    def test_get_users_by_role_insufficient_permissions(self, client, get_user_token):
        """
        Test: Accès avec un token USER (permissions insuffisantes)
        - Doit retourner 403
        - Note: Tu devras peut-être créer un fixture get_user_token
        """
        # Act: Appeler avec un token USER
        response = client.get(
            f'{BASE_API_URL}/users/role/ADMIN',
            headers={'Authorization': f'Bearer {get_user_token["token"]}'}
        )

        # Assert
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        assert 'permission' in data['error'].lower()

    def test_get_users_by_role_case_insensitive(self, client, redis_client, get_admin_token):
        """
        Test: Le filtre de rôle est insensible à la casse
        - 'admin', 'ADMIN', 'Admin' devraient tous fonctionner
        """
        # Arrange: Créer un admin
        admin_user = {"firstname": "Admin", "lastname": "Test", "email": "admin@test.com", "password": "Password123", "role": "ADMIN"}
        client.post(f'{BASE_API_URL}/register', json=admin_user)

        # Act: Filtrer avec différentes casses
        for role_variant in ['admin', 'ADMIN', 'Admin']:
            response = client.get(
                f'{BASE_API_URL}/users/role/{role_variant}',
                headers={'Authorization': f'Bearer {get_admin_token["token"]}'}
            )
            
            # Assert: Toutes les variantes doivent retourner des résultats
            assert response.status_code == 200
            data = response.get_json()
            assert data['count'] >= 2  # Au moins l'admin fixture + l'admin créé


# Fixture supplémentaire pour les tests de permissions
@pytest.fixture
def get_user_token(client):
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
    login_response = client.post(f'{BASE_API_URL}/login', json=user_data)
    assert login_response.status_code == 200
    user = login_response.get_json()['user']
    
    return user