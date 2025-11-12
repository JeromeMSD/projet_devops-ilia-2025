from main import db
from main import app as flask_app
import pytest
import json


# Fonction qui va crée un faux client qui va pouvoir simuler des requêtes HTML (GET, POST)

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        # On remet à zéro la base de données avant CHAQUE test.
        db['incidents'] = {}
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

    response = client.post(
        '/api/v1/incidents', data=json.dumps(incident_data), content_type='application/json')

    # Vérifie le statut (201=Created)
    assert response.status_code == 201

    # Vérifie le contenu de la réponse
    json_data = response.get_json()
    assert json_data['title'] == "API Lente"
    assert json_data['sev'] == 2
    assert json_data['status'] == "open"  # Statut par défaut
    assert json_data['commander'] is None  # Personne assigné au début
    assert 'id' in json_data
    assert 'started_at' in json_data

    # Vérifie que c'est bien sauvegardé dans notre "db"
    assert len(db['incidents']) == 1
    assert list(db['incidents'].values())[0]['title'] == "API Lente"


# Va tester la création d'un incident qui échoue (par exemple données manquantes comme ici)
def test_create_incident_fail_missing_sev(client):
    # Il manque "sev" (requis par le Swagger)
    incident_data = {"title": "API Lente"}

    response = client.post(
        '/api/v1/incidents', data=json.dumps(incident_data), content_type='application/json')

    # Vérifie le statut (400=Bad Request)
    assert response.status_code == 400
    assert "error" in response.get_json()
    print(db)
    assert len(db['incidents']) == 0  # Rien ne doit être sauvegardé


# Va tester les filtres "commander" et "status" pour les incidents
def test_get_incidents_with_filters(client):

    # On simule dans notre base de données des données de test
    inc1 = {"id": "INC-1", "title1": "A", "status": "open",
            "sev": 1, "commander": "user-aurelien"}
    inc2 = {"id": "INC-2", "title2": "B", "status": "resolved",
            "sev": 2, "commander": "user-aurelien"}
    inc3 = {"id": "INC-3", "title3": "C", "status": "open",
            "sev": 1, "commander": "user-thomas"}
    db['incidents'] = {
        "INC-1": inc1,
        "INC-2": inc2,
        "INC-3": inc3
    }

    # Test filtre : Status
    response_status = client.get('/api/v1/incidents?status=open')
    assert response_status.status_code == 200
    data_status = response_status.get_json()
    assert len(data_status) == 2  # INC-1 et INC-3
    assert data_status[0]['id'] == "INC-1"
    assert data_status[1]['id'] == "INC-3"

    # Test filtre : Commander
    response_commander = client.get(
        '/api/v1/incidents?commander=user-aurelien')
    assert response_commander.status_code == 200
    data_commander = response_commander.get_json()
    assert len(data_commander) == 2  # INC-1 et INC-2
    assert data_commander[0]['id'] == "INC-1"
    assert data_commander[1]['id'] == "INC-2"


def test_get_incident_by_id(client):
    # Crée d'abord un incident (pour avoir un ID connu)
    payload = {
        "title": "API Latency EU",
        "sev": 3,
        "services": ["api"],
        "summary": "High latency detected in EU-West"
    }
    create_response = client.post("/api/v1/incidents", json=payload)
    created = create_response.get_json()
    incident_id = created["id"]

    # Récupère l'incident créé
    response = client.get(f"/api/v1/incidents/{incident_id}")

    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == incident_id
    assert data["title"] == payload["title"]

    # Teste un incident qui n'existe pas
    response_404 = client.get("/api/v1/incidents/INC-DOESNOTEXIST")
    assert response_404.status_code == 404


def test_update_incident_status(client):
    # Créer un incident temporaire
    db["incidents"]["INC-999"] = {
        "id": "INC-999",
        "title": "Test incident",
        "sev": 2,
        "status": "open",
        "services": ["api"],
        "summary": "Test summary"
    }

    # Test mise à jour du status
    response = client.post(
        '/api/v1/incidents/INC-999/status',
        json={"status": "resolved"}
    )
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "resolved"

    # Test incident inexistant
    response = client.post(
        '/api/v1/incidents/INC-404/status',
        json={"status": "mitigated"}
    )
    assert response.status_code == 404
