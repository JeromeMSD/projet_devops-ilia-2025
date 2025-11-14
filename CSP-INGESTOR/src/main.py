from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import json
import os
import requests

app = FastAPI(title="PolyStatus - CSP Ingestor API")

# -------------------------
# Redis connection
# -------------------------
r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),  
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

# -------------------------
# Models
# -------------------------
class ProviderCreate(BaseModel):
    name: str
    feed_url: str
    type: str  # "json" or "rss" (we only support json for now)

# -------------------------
# Endpoint: Register provider
# -------------------------
@app.post("/api/v1/csp/providers", status_code=201)
def add_provider(provider: ProviderCreate):
    data = provider.model_dump()
    r.hset("csp:providers", provider.name.lower(), json.dumps(data))
    return {"message": "Provider enregistré avec succès"}

# -------------------------
# Endpoint: Refresh events from provider
# -------------------------
@app.post("/api/v1/csp/refresh")
def refresh_provider(provider: str):
    provider = provider.lower()

    raw = r.hget("csp:providers", provider)
    if raw is None:
        raise HTTPException(status_code=404, detail="Provider not found")

    cfg = json.loads(raw)

    try:
        resp = requests.get(cfg["feed_url"], timeout=10)
        data = resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch feed: {e}")

    # Extract some sample fields (depends on actual Cloudflare API)
    events = []
    for component in data.get("components", []):
        events.append({
            "provider": provider,
            "service": component.get("name"),
            "status": component.get("status")
        })

    # Store events in redis LIST
    r.delete(f"csp:events:{provider}")
    for ev in events:
        r.rpush(f"csp:events:{provider}", json.dumps(ev))

    return {"message": f"Refreshed {len(events)} events", "events": events}

# -------------------------
# Endpoint: Get events
# -------------------------
@app.get("/api/v1/csp/events")
def list_events():
    all_events = []
    keys = r.keys("csp:events:*")
    for k in keys:
        for raw in r.lrange(k, 0, -1):
            all_events.append(json.loads(raw))
    return all_events
