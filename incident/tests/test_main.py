import pytest
import sys
import os
import json 

# Va aller chercher le dossier src, la ou se trouve le main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import app as flask_app
from main import db  

# Fonction qui va crée un faux client qui va pouvoir simuler des requêtes HTML (GET, POST)
@pytest.fixture 
def client():
    with flask_app.test_client() as client:
        db['incidents'] = {} # On remet à zéro la base de données avant CHAQUE test.
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


# Va tester la création d'un incident avec succès (POST)
def test_create_incident_success(client):

    # Le JSON qu'on envoie pour créer un incident
    incident_data = {
        "title": "API Lente",
        "sev": 2,
        "services": ["api", "db"]
    }
    
    response = client.post('/api/v1/incidents', data=json.dumps(incident_data), content_type='application/json')
    
    # Vérifie le statut (201=Created)
    assert response.status_code == 201
    
    # Vérifie le contenu de la réponse
    json_data = response.get_json()
    assert json_data['title'] == "API Lente"
    assert json_data['sev'] == 2
    assert json_data['status'] == "open" # Statut par défaut
    assert json_data['commander'] is None # Personne assigné au début
    assert 'id' in json_data
    assert 'started_at' in json_data
    
    # Vérifie que c'est bien sauvegardé dans notre "db"
    assert len(db['incidents']) == 1
    assert list(db['incidents'].values())[0]['title'] == "API Lente"


# Va tester la création d'un incident qui échoue (par exemple données manquantes comme ici)
def test_create_incident_fail_missing_sev(client):
    incident_data = { "title": "API Lente" }  # Il manque "sev" (requis par le Swagger)
    
    response = client.post('/api/v1/incidents', data=json.dumps(incident_data), content_type='application/json')
    
    # Vérifie le statut (400=Bad Request)
    assert response.status_code == 400
    assert "error" in response.get_json()
    print(db)
    assert len(db['incidents']) == 0 # Rien ne doit être sauvegardé