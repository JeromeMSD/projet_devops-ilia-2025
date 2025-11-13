import json
import pytest
from main import app, r

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


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
    redis_obj = r.get(data["id"])
    assert redis_obj is not None


def test_create_invalid_incident(client):
    """Teste la création d’un incident invalide (manque 'title' ou 'sev')."""
    response = client.post(
        '/api/v1/incidents',
        data=json.dumps({"title": "Missing sev"}),
        content_type='application/json'
    )
    assert response.status_code == 400


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
    assert all(inc["status"] == "open" for inc in data)
