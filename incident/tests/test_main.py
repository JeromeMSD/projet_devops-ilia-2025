import json
import pytest
from main import app, saveJSONFile, loadJSONFile
from redis_link import *

@pytest.fixture
def client():
    """
    Crée un client de test Flask isolé pour simuler des requêtes HTTP.
    Le client s'exécute dans un contexte 'TESTING' sans lancer le vrai serveur.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# === TESTS DE BASE ===

def test_redis_connection():
    """Vérifie que Redis est bien accessible et répond au ping."""
    assert r.ping() is True


def test_health_check(client):
    """Teste la route de health check."""
    response = client.get('/api/v1/incidents/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["redis"] == "connected"


# === TESTS DE CREATION ===

def test_create_incident(client):
    """Teste la création d’un incident valide."""
    incident_data = {
        "title": "Test incident",
        "sev": "high",
        "summary": "Problème de test"
    }
    response = client.post(
        '/api/v1/incidents',
        data=json.dumps(incident_data),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["status"] == "open"

    # Vérifie que l’incident est bien stocké dans Redis
    redis_obj = r.get(f"INC:{data['id']}") or r.get(data["id"])
    assert redis_obj is not None


def test_create_invalid_incident(client):
    """Teste la création d’un incident invalide (manque 'title' ou 'sev')."""
    response = client.post(
        '/api/v1/incidents',
        data=json.dumps({"title": "Missing sev"}),
        content_type='application/json'
    )
    assert response.status_code == 400


# === TESTS DE LECTURE ===

def test_get_all_incidents(client):
    """Teste la récupération de tous les incidents."""
    response = client.get('/api/v1/incidents')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert all("id" in inc for inc in data)


def test_get_incident_by_id(client):
    """Crée un incident puis le récupère par ID."""
    new_incident = {
        "title": "Incident to retrieve",
        "sev": "low"
    }
    create_resp = client.post(
        '/api/v1/incidents',
        data=json.dumps(new_incident),
        content_type='application/json'
    )
    created_data = create_resp.get_json()
    inc_id = created_data["id"]

    get_resp = client.get(f'/api/v1/incidents/{inc_id}')
    assert get_resp.status_code == 200
    retrieved_data = get_resp.get_json()
    assert retrieved_data["id"] == inc_id
    assert retrieved_data["title"] == "Incident to retrieve"


def test_filter_by_status(client):
    """Teste le filtre 'status=open' sur la route GET /incidents."""
    response = client.get('/api/v1/incidents?status=open')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    for inc in data:
        assert inc["status"] == "open"


# === TESTS DE MISE À JOUR ===

def test_update_incident_status(client):
    """Teste la mise à jour du statut d’un incident."""
    # Création d’un incident
    create_resp = client.post(
        '/api/v1/incidents',
        json={"title": "Test update status", "sev": "medium"}
    )
    inc = create_resp.get_json()
    inc_id = inc["id"]

    # Mise à jour du statut
    response = client.put(
        f'/api/v1/incidents/{inc_id}/status',
        json={"status": "resolved"}
    )
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "resolved"

    # Incident inexistant
    response_404 = client.put(
        '/api/v1/incidents/INC-UNKNOWN/status',
        json={"status": "mitigated"}
    )
    assert response_404.status_code == 404


def test_assign_incident(client):
    """Teste l'assignation d'un commandant à un incident."""
    payload = {
        "title": "Database outage",
        "sev": "2",
        "services": ["db"],
        "summary": "Primary DB unavailable"
    }
    create_response = client.post("/api/v1/incidents", json=payload)
    created = create_response.get_json()
    incident_id = created["id"]

    # Cas normal : assigner un user
    assign_payload = {"commander": "thomas"}
    response = client.put(
        f"/api/v1/incidents/{incident_id}/assign", json=assign_payload)
    assert response.status_code == 200

    updated = response.get_json()
    assert updated["commander"] == "thomas"

    # Cas invalide : pas de champ commander
    response_invalid = client.put(
        f"/api/v1/incidents/{incident_id}/assign", json={})
    assert response_invalid.status_code == 400

    # Cas incident inexistant
    response_404 = client.put(
        "/api/v1/incidents/INC-UNKNOWN/assign", json=assign_payload)
    assert response_404.status_code == 404


def test_add_timeline_event(client):
    """Teste l'ajout d’un événement dans la timeline."""
    # Création d’un incident
    create_resp = client.post(
        '/api/v1/incidents',
        json={"title": "Timeline test", "sev": "medium"}
    )
    inc = create_resp.get_json()
    inc_id = inc["id"]

    # Ajout d’un événement à la timeline
    response = client.put(
        f'/api/v1/incidents/{inc_id}/timeline',
        json={"type": "alert", "message": "CPU spike detected"}
    )
    assert response.status_code == 200
    updated = response.get_json()
    assert "timeline" in updated
    assert any(event["type"] == "alert" for event in updated["timeline"])

    # Cas invalide : champ manquant
    response_invalid = client.put(
        f'/api/v1/incidents/{inc_id}/timeline',
        json={"type": "alert"}
    )
    assert response_invalid.status_code == 400


def test_add_postmortem(client):
    """Teste l’ajout d’un postmortem à un incident."""
    # Création d’un incident
    create_resp = client.post(
        '/api/v1/incidents',
        json={"title": "Postmortem test", "sev": "medium"}
    )
    inc = create_resp.get_json()
    inc_id = inc["id"]

    postmortem_data = {
        "what_happened": "Service down due to overload",
        "root_cause": "Traffic spike",
        "action_items": ["Add autoscaling", "Improve caching"]
    }

    response = client.put(
        f'/api/v1/incidents/{inc_id}/postmortem',
        json=postmortem_data
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "postmortem" in data
    assert data["postmortem"]["root_cause"] == "Traffic spike"

    # Cas invalide : champs manquants
    response_invalid = client.put(
        f'/api/v1/incidents/{inc_id}/postmortem',
        json={"what_happened": "Oops"}
    )
    assert response_invalid.status_code == 400
