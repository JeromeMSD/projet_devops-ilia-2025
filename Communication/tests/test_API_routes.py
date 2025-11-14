import pytest
import json
import sys
import os
from app import app

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.insert(0, src_dir)


from API_routes import app 

@pytest.fixture
def client():
    #Crée un client de test pour l'application Flask.
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_send_email_route(client):
    
    #Test 1 (RED): Vérifie que la route /api/v1/email existe, accepte un POST, et renvoie un succès.
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
    
    
def test_CreateAnnoucement():
    
    test_message = {
        "message":"Test annonce API"
        "etat": "en cours"
    }

    response = client.post(
        "api/v1/public/announce",
        data = json.dumps(test_message),
        content_type="application/json"
    )

    assert response.status_code == 201

    data = response.get_json()

    assert "message" in data
    assert data["message"] == "Annonce bien enregistrée"
    assert "announce in data"

    annonces = redis_client.lrange("annonces",0,-1)
    assert len(annonces) == 1
    annonces2= json.dumps(annonces[0])

    assert annonces2["message"] == message["message"]
    assert annonces2["etat"] == message["etat"]

#vérifie que la route api/status renvoie le bon format de données
def test_status_api_format():
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.get("/api/v1/public/status")

    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, dict)

    assert "status" in data
    assert "count" in data
    assert "data" in data

    assert isinstance(data["status"], str)
    assert isinstance(data["count"], int)
    assert isinstance(data["data"], list)
    

def test_register_webhook(client):
    response = client.post("/api/v1/webhooks", json={
        "url": "http://example.com",
        "event_type": "incident"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "webhook" in data
    assert data["webhook"]["url"] == "http://example.com"
