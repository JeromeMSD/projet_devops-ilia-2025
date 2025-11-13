import pytest
from src.API_webhook import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_webhook(client):
    response = client.post("/api/v1/webhooks", json={
        "url": "http://example.com",
        "event_type": "incident"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "webhook" in data
    assert data["webhook"]["url"] == "http://example.com"
