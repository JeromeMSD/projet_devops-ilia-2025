from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_add_cloudflare_provider_returns_201(monkeypatch):
    """Register the real Cloudflare provider."""

    provider_data = {
        "name": "cloudflare",
        "feed_url": "https://www.cloudflarestatus.com/api/v2/incidents.json",
        "type": "json"
    }

    response = client.post("/api/v1/csp/providers", json=provider_data)

    assert response.status_code == 201
    assert response.json()["message"] == "Provider enregistré avec succès"
