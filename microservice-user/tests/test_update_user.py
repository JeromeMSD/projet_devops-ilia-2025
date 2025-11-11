import pytest
import os

BASE_API_URL = os.getenv('BASE_API_URL')

# Fixtures COMPLÈTES et AUTONOMES


@pytest.fixture
def sample_admin_user():
    return {
        "firstname": "Admin",
        "lastname": "Test",
        "email": "admin@test.com",
        "password": "Password123",
        "role": "ADMIN"
    }


@pytest.fixture
def sample_user():
    return {
        "firstname": "Regular",
        "lastname": "User",
        "email": "user@test.com",
        "password": "Password123",
        "role": "USER"
    }


@pytest.fixture
def get_admin_token(client, sample_admin_user, redis_client):
    """Create and login admin user"""
    client.post(f'{BASE_API_URL}/register', json=sample_admin_user)
    login_response = client.post(f'{BASE_API_URL}/login', json={
        "email": sample_admin_user["email"],
        "password": sample_admin_user["password"]
    })
    return login_response.get_json()['user']


@pytest.fixture
def get_user_token(client, sample_user, redis_client):
    """Create and login regular user"""
    client.post(f'{BASE_API_URL}/register', json=sample_user)
    login_response = client.post(f'{BASE_API_URL}/login', json={
        "email": sample_user["email"],
        "password": sample_user["password"]
    })
    return login_response.get_json()['user']


@pytest.fixture
def get_sre_token(client, redis_client):
    """Create and login SRE user"""
    sre_data = {
        "firstname": "SRE",
        "lastname": "Engineer",
        "email": "sre@test.com",
        "password": "Password123",
        "role": "SRE"
    }
    client.post(f'{BASE_API_URL}/register', json=sre_data)
    login_response = client.post(f'{BASE_API_URL}/login', json={
        "email": sre_data["email"],
        "password": sre_data["password"]
    })
    return login_response.get_json()['user']


class TestUpdateUser:
    """Tests pour la modification d'utilisateur"""

    def test_update_user_success_admin(self, client, get_admin_token, test_user):
        """Test: ADMIN peut modifier un utilisateur"""
        user_to_update = test_user['user']
        update_data = {
            "firstname": "NouveauPrenom",
            "lastname": "NouveauNom",
            "role": "SRE"
        }
        response = client.put(
            f"{BASE_API_URL}/users/{user_to_update.id_user}",
            json=update_data,
            headers={'Authorization': f'Bearer {get_admin_token["token"]}'}
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['user']['firstname'] == "NouveauPrenom"
        assert data['user']['lastname'] == "NouveauNom"
        assert data['user']['role'] == "SRE"

    def test_update_user_unauthorized_user(self, client, get_user_token, test_user):
        """Test: USER ne peut pas modifier un autre utilisateur"""
        user_to_update = test_user['user']
        response = client.put(
            f"{BASE_API_URL}/users/{user_to_update.id_user}",
            json={"firstname": "Nouveau"},
            headers={'Authorization': f'Bearer {get_user_token["token"]}'}
        )
        assert response.status_code == 403

    def test_update_user_not_found(self, client, get_admin_token):
        """Test: Modifier un utilisateur inexistant"""
        response = client.put(
            f"{BASE_API_URL}/users/invalid-id",
            json={"firstname": "Nouveau"},
            headers={'Authorization': f'Bearer {get_admin_token["token"]}'}
        )
        assert response.status_code == 404

    def test_update_user_sre_can_update(self, client, get_sre_token, test_user):
        """Test: SRE peut modifier un utilisateur"""
        user_to_update = test_user['user']
        response = client.put(
            f"{BASE_API_URL}/users/{user_to_update.id_user}",
            json={"firstname": "UpdatedBySRE"},
            headers={'Authorization': f'Bearer {get_sre_token["token"]}'}
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['user']['firstname'] == "UpdatedBySRE"
