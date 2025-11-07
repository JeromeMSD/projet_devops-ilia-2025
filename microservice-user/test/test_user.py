"""
Test suite for User Microservice API
Run with: pytest tests/test_user.py -v
"""
import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app, users_db


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    # Clean up after each test
    users_db.clear()


@pytest.fixture
def sample_user():
    """Sample user data for testing"""
    return {
        "username": "test_user",
        "email": "test@example.com",
        "password": "password123",
        "role": "user"
    }


class TestHealthCheck:
    """Test health check endpoint"""

    def test_health_check(self, client):
        """Test GET /health returns 200 and correct response"""
        response = client.get('/health')

        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert data['service'] == 'user-microservice'


class TestUserCreation:
    """Test user creation endpoint"""

    def test_create_user_success(self, client, sample_user):
        """Test successful user creation"""
        response = client.post('/api/v1/users', json=sample_user)

        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'User created successfully'
        assert data['user']['username'] == sample_user['username']
        assert data['user']['email'] == sample_user['email']
        assert data['user']['role'] == sample_user['role']
        assert 'user_id' in data['user']
        assert 'created_at' in data['user']
        # Password hash should not be in response
        assert 'password_hash' not in data['user']

    def test_create_user_missing_fields(self, client):
        """Test user creation with missing required fields"""
        # Missing password
        incomplete_user = {
            "username": "test_user",
            "email": "test@example.com"
        }
        response = client.post('/api/v1/users', json=incomplete_user)

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data


    def test_create_user_invalid_email(self, client):
        """Test user creation with invalid email"""
        invalid_user = {
            "username": "test_user",
            "email": "invalid-email",  # No @ sign
            "password": "password123"
        }
        response = client.post('/api/v1/users', json=invalid_user)

        assert response.status_code == 400

    def test_create_user_short_username(self, client):
        """Test user creation with username too short"""
        invalid_user = {
            "username": "ab",  # Less than 3 characters
            "email": "test@example.com",
            "password": "password123"
        }
        response = client.post('/api/v1/users', json=invalid_user)

        assert response.status_code == 400


class TestUserLogin:
    """Test user authentication/login endpoint"""

    def test_login_success(self, client, sample_user):
        """Test successful login"""
        # Create user first
        client.post('/api/v1/users', json=sample_user)

        # Login
        login_data = {
            "username": sample_user['username'],
            "password": sample_user['password']
        }
        response = client.post('/api/v1/auth/login', json=login_data)

        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Login successful'
        assert 'token' in data
        assert data['user']['username'] == sample_user['username']

    def test_login_wrong_password(self, client, sample_user):
        """Test login with incorrect password"""
        # Create user
        client.post('/api/v1/users', json=sample_user)

        # Try to login with wrong password
        login_data = {
            "username": sample_user['username'],
            "password": "wrong_password"
        }
        response = client.post('/api/v1/auth/login', json=login_data)

        assert response.status_code == 401
        data = response.get_json()
        assert 'Invalid credentials' in data['error']

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent username"""
        login_data = {
            "username": "nonexistent_user",
            "password": "password123"
        }
        response = client.post('/api/v1/auth/login', json=login_data)

        assert response.status_code == 401
        data = response.get_json()
        assert 'Invalid credentials' in data['error']

    def test_login_missing_credentials(self, client):
        """Test login with missing credentials"""
        # Missing password
        response = client.post('/api/v1/auth/login', json={"username": "test"})

        assert response.status_code == 400


class TestGetUsers:
    """Test get all users endpoint"""

    def test_get_users_empty(self, client):
        """Test getting users when database is empty"""
        response = client.get('/api/v1/users')

        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 0
        assert data['users'] == []

    def test_get_users_with_data(self, client, sample_user):
        """Test getting users when users exist"""
        # Create a user
        client.post('/api/v1/users', json=sample_user)

        # Create another user
        user2 = {
            "username": "user2",
            "email": "user2@example.com",
            "password": "password456",
            "role": "sre"
        }
        client.post('/api/v1/users', json=user2)

        # Get all users
        response = client.get('/api/v1/users')

        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 2
        assert len(data['users']) == 2


class TestGetUserById:
    """Test get user by ID endpoint"""

    def test_get_user_by_id_success(self, client, sample_user):
        """Test getting a user by valid ID"""
        # Create user
        create_response = client.post('/api/v1/users', json=sample_user)
        created_user = create_response.get_json()['user']
        user_id = created_user['user_id']

        # Get user by ID
        response = client.get(f'/api/v1/users/{user_id}')

        assert response.status_code == 200
        data = response.get_json()
        assert data['user_id'] == user_id
        assert data['username'] == sample_user['username']

    def test_get_user_by_invalid_id(self, client):
        """Test getting a user with invalid ID"""
        response = client.get('/api/v1/users/INVALID-ID-123')

        assert response.status_code == 404
        data = response.get_json()
        assert 'not found' in data['error'].lower()


class TestUpdateUser:
    """Test update user endpoint"""

    def test_update_user_email(self, client, sample_user):
        """Test updating user email"""
        # Create user and login
        create_response = client.post('/api/v1/users', json=sample_user)
        user_id = create_response.get_json()['user']['user_id']

        login_response = client.post('/api/v1/auth/login', json={
            "username": sample_user['username'],
            "password": sample_user['password']
        })
        token = login_response.get_json()['token']

        # Update email
        update_data = {"email": "newemail@example.com"}
        response = client.put(
            f'/api/v1/users/{user_id}',
            json=update_data,
            headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['user']['email'] == "newemail@example.com"


class TestIntegration:
    """Integration tests - testing full user workflows"""

    def test_full_user_workflow(self, client):
        """Test complete user workflow: create -> login -> get -> update"""
        # 1. Create user
        user_data = {
            "username": "workflow_user",
            "email": "workflow@example.com",
            "password": "secure_pass_123",
            "role": "user"
        }
        create_response = client.post('/api/v1/users', json=user_data)
        assert create_response.status_code == 201
        user_id = create_response.get_json()['user']['user_id']

        # 2. Login
        login_response = client.post('/api/v1/auth/login', json={
            "username": user_data['username'],
            "password": user_data['password']
        })
        assert login_response.status_code == 200
        token = login_response.get_json()['token']

        # 3. Get user by ID
        get_response = client.get(f'/api/v1/users/{user_id}')
        assert get_response.status_code == 200
        assert get_response.get_json()['username'] == user_data['username']

        # 4. Get all users
        all_users_response = client.get('/api/v1/users')
        assert all_users_response.status_code == 200
        assert all_users_response.get_json()['count'] >= 1

        # 5. Update user
        update_response = client.put(
            f'/api/v1/users/{user_id}',
            json={"email": "updated@example.com"},
            headers={'Authorization': f'Bearer {token}'}
        )
        assert update_response.status_code == 200
        assert update_response.get_json()['user']['email'] == "updated@example.com"


