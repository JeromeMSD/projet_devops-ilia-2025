import pytest
import sys
import os

# Va aller chercher le dossier src, la ou se trouve le main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import app as flask_app

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