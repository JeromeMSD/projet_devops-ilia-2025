import pytest
import sys
import os

# Va aller chercher le dossier src, la ou se trouve le main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import app as flask_app, db


# Fonction qui va crée un faux client qui va pouvoir simuler des requêtes HTML (GET, POST)
@pytest.fixture 
def client():
    with flask_app.test_client() as client:
        yield client

# Va tester la route /health pour s'assurer qu'elle répond 200 OK et retourne le bon JSON
def test_health_check(client):
    response = client.get('/api/v1/incidents/health')
    
    # Vérifie le code de statut HTTP
    assert response.status_code == 200
    
    # Vérifie le contenu de la réponse JSON
    json_data = response.get_json()
    assert json_data == {
        "status": "ok",
        "service": "incidents"
    }


# Va tester la route GET /incidents et verifie qu'elle retourne une liste vide au début
def test_get_incidents_empty(client):
    response = client.get('/api/v1/incidents')
    
    # Vérifie le code de statut HTTP
    assert response.status_code == 200
    
    # Vérifie que la réponse est une liste vide
    json_data = response.get_json()
    assert json_data == []

def test_add_timeline_event(client):
    # Créer un incident temporaire
    db["incidents"]["INC-888"] = {
        "id": "INC-888",
        "title": "Incident timeline test",
        "sev": 2,
        "status": "open",
        "services": ["api"],
        "summary": "Testing timeline",
        "timeline": []  # On initialise la timeline
    }

    # Ajouter un événement
    event = {"type": "note", "message": "Premier test de note"}
    response = client.post(
        '/api/v1/incidents/INC-888/timeline',
        json=event
    )
    assert response.status_code == 200
    json_data = response.get_json()
    assert "timeline" in json_data
    assert json_data["timeline"][0] == event

    # Cas incident inexistant
    response = client.post(
        '/api/v1/incidents/INC-404/timeline',
        json=event
    )
    assert response.status_code == 404


def test_postmortem_incident(client):
    # Créer un incident temporaire
    db["incidents"]["INC-777"] = {
        "id": "INC-777",
        "title": "Incident postmortem test",
        "sev": 2,
        "status": "open",
        "services": ["api"],
        "summary": "Testing postmortem"
    }

    # Corps JSON du postmortem
    postmortem_data = {
        "what_happened": "Panne API",
        "root_cause": "Erreur de configuration",
        "action_items": ["Redémarrer service", "Mettre à jour config"]
    }

    # Ajouter ou modifier le postmortem
    response = client.post(
        '/api/v1/incidents/INC-777/postmortem',
        json=postmortem_data
    )
    assert response.status_code == 200
    json_data = response.get_json()
    assert "postmortem" in json_data
    assert json_data["postmortem"] == postmortem_data

    # Cas incident inexistant
    response = client.post(
        '/api/v1/incidents/INC-404/postmortem',
        json=postmortem_data
    )
    assert response.status_code == 404