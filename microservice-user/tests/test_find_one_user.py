import pytest
import json
from flask import Flask
from unittest.mock import patch
from src.routes.find_one_user import one_user_bp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(one_user_bp)
    app.testing = True
    with app.test_client() as client:
        yield client

def test_get_user_by_id_success(client):
    fake_user = {"id_user":"123","firstname":"Vanelle","lastname":"Axpertia","email":"vanelle@example.com","role":"USER"}
    with patch('src.redis_client.get_redis_client') as mock_redis_client:
        mock_redis = mock_redis_client.return_value
        mock_redis.exists.return_value = True
        mock_redis.get.return_value = json.dumps(fake_user)
        response = client.get('/users/123')
        assert response.status_code == 200
        data = response.get_json()
        assert data['user']['email'] == "vanelle@example.com"

def test_get_user_by_id_not_found(client):
    with patch('src.redis_client.get_redis_client') as mock_redis_client:
        mock_redis = mock_redis_client.return_value
        mock_redis.exists.return_value = False
        response = client.get('/users/999')
        assert response.status_code == 404

def test_get_all_users(client):
    fake_users = [
        {"id_user":"123","firstname":"Vanelle"},
        {"id_user":"456","firstname":"Alice"}
    ]
    with patch('src.redis_client.get_redis_client') as mock_redis_client:
        mock_redis = mock_redis_client.return_value
        mock_redis.keys.return_value = ["user:123","user:456"]
        mock_redis.get.side_effect = [json.dumps(fake_users[0]), json.dumps(fake_users[1])]
        response = client.get('/users')
        data = response.get_json()
        assert response.status_code == 200
        assert len(data['users']) == 2
