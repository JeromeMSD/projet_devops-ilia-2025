import json
from fastapi.testclient import TestClient
from unittest.mock import patch
import fakeredis

from src.main import app, r as real_redis

# ---------------------------
# FIXTURES
# ---------------------------

def setup_module(module):
    """Use FakeRedis instead of the real one."""
    fake = fakeredis.FakeRedis(decode_responses=True)
    # monkeypatch global redis instance in main.py
    module._orig_redis = real_redis
    globals()['real_redis'] = fake


def teardown_module(module):
    """Restore real Redis if needed."""
    globals()['real_redis'] = module._orig_redis


client = TestClient(app)


# ---------------------------
# TEST: POST /providers
# ---------------------------
def test_add_provider():
    payload = {
        "name": "cloudflare",
        "feed_url": "https://example.com/feed.json",
        "type": "json"
    }

    response = client.post("/api/v1/csp/providers", json=payload)
    assert response.status_code == 201

    # Validate redis storage
    stored = real_redis.hget("csp:providers", "cloudflare")
    assert stored is not None

    parsed = json.loads(stored)
    assert parsed["feed_url"] == payload["feed_url"]


# ---------------------------
# TEST: POST /refresh
# ---------------------------
@patch("CSP_INGESTOR.src.main.requests.get")
def test_refresh_provider(mock_get):
    """Refresh should fetch data from external API and store parsed events."""

    # Prepare fake provider in redis
    real_redis.hset(
        "csp:providers",
        "cloudflare",
        json.dumps({
            "name": "cloudflare",
            "feed_url": "https://fake-url.com/api.json",
            "type": "json"
        })
    )

    # Fake API response
    mock_get.return_value.json.return_value = {
        "components": [
            {"name": "API", "status": "operational"},
            {"name": "CDN", "status": "degraded_performance"}
        ]
    }

    response = client.post("/api/v1/csp/refresh?provider=cloudflare")
    assert response.status_code == 200

    data = response.json()
    assert data["message"].startswith("Refreshed")
    assert len(data["events"]) == 2

    # Redis should now contain 2 events
    events = real_redis.lrange("csp:events:cloudflare", 0, -1)
    assert len(events) == 2


# ---------------------------
# TEST: GET /events
# ---------------------------
def test_get_events():
    """Get all events from all providers."""

    # Insert example data
    real_redis.rpush("csp:events:cloudflare", json.dumps({
        "provider": "cloudflare",
        "service": "API",
        "status": "operational"
    }))

    response = client.get("/api/v1/csp/events")
    assert response.status_code == 200

    events = response.json()
    assert len(events) >= 1
    assert events[0]["provider"] == "cloudflare"
