import pytest
import json
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.insert(0, src_dir)


from API_routes import app 

@pytest.fixture
def client():
    """Crée un client de test pour l'application Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_send_email_route(client):
    """
    Test 1 (RED): Vérifie que la route /api/v1/email existe,
    accepte un POST, et renvoie un succès.
    """
    email_data = {
        "to": "destinataire@example.com",
        "subject": "Sujet du test",
        "body": "Ceci est un email de test."
    }
    
    response = client.post('/api/v1/email', json=email_data)
    
    
    assert response.status_code == 200
    
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Email simulé envoyé avec succès"
