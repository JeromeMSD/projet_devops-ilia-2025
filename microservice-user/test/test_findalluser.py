"""
Test suite for Find All Users endpoint
Run with: pytest test/test_findalluser.py -v
"""
import pytest
import sys
import os

# Add src directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_dir)

from main import create_app
from redis_client import get_redis_client


@pytest.fixture
def app():
    """Create Flask application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create a test client for the Flask app"""
    with app.test_client() as client:
        yield client
    # Clean up Redis after each test
    redis_client = get_redis_client()
    if redis_client:
        keys = redis_client.keys('user:*')
        if keys:
            redis_client.delete(*keys)


@pytest.fixture
def sample_user():
    """Sample user data for testing"""
    return {
        "firstname": "John",
        "lastname": "Doe",
        "email": "john.doe@example.com",
        "password": "securePassword123",
        "role": "user"
    }


class TestFindAllUsers:
    """Test find all users endpoint"""

    def test_users_attributes_not_empty(self, client, sample_user):
        """
        Test that all user attributes are not empty
        Verify: firstname, lastname, email, role, id_user, token, created_at are all present and not empty
        """
        # Create a user first
        create_response = client.post('/api/v1/users', json=sample_user)
        assert create_response.status_code == 201

        # Get all users
        response = client.get('/api/v1/users')
        assert response.status_code == 200

        data = response.get_json()
        assert 'users' in data
        assert len(data['users']) > 0

        # Check each user has non-empty attributes
        for user in data['users']:
            # Firstname should not be empty
            assert 'firstname' in user
            assert user['firstname'] is not None
            assert user['firstname'] != ""

            # Lastname should not be empty
            assert 'lastname' in user
            assert user['lastname'] is not None
            assert user['lastname'] != ""

            # Email should not be empty
            assert 'email' in user
            assert user['email'] is not None
            assert user['email'] != ""

            # Role should not be empty
            assert 'role' in user
            assert user['role'] is not None
            assert user['role'] != ""

            # ID should not be empty
            assert 'id_user' in user
            assert user['id_user'] is not None
            assert user['id_user'] != ""

            # Token should not be empty
            assert 'token' in user
            assert user['token'] is not None
            assert user['token'] != ""

            # Created_at should not be empty
            assert 'created_at' in user
            assert user['created_at'] is not None
            assert user['created_at'] != ""

            # Password should NOT be in the response
            assert 'password' not in user

    def test_get_all_users_empty(self, client):
        """Test getting all users when database is empty"""
        response = client.get('/api/v1/users')

        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 0
        assert data['users'] == []

    

    


