from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
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

    raw_provider = r.hget("csp:providers", provider)
    if not raw_provider:
        return {"error": "Provider not found"}

    provider_data = json.loads(raw_provider)
    feed_url = provider_data["feed_url"]
    ptype = provider_data["type"]

    # --- RESET EVENTS FOR THIS PROVIDER ---
    r.delete(f"csp:events:{provider}")

    # --- FETCH DATA ---
    import requests
    resp = requests.get(feed_url)
    data = resp.json()

    # --- EXTRACT EVENTS ---
    events = []
    for comp in data["components"]:
        events.append({
            "provider": provider,
            "service": comp["name"],
            "status": comp["status"]
        })

    # --- STORE CLEAN EVENTS ---
    for e in events:
        r.rpush(f"csp:events:{provider}", json.dumps(e))

    return {"message": f"Refreshed {len(events)} events", "provider": provider}


# -------------------------
# Endpoint: Get events
# -------------------------
@app.get("/api/v1/csp/events")
def get_events(active: bool = False):
# Return all CSP events across providers. 
# If active=true, only non-operational statuses are returned.
    
    events = []

    # Find all keys containing events
    keys = r.keys("csp:events:*")

    for key in keys:
        provider = key.split(":")[-1]  # extract provider name
        raw_list = r.lrange(key, 0, -1)

        for item in raw_list:
            event = json.loads(item)

            if active:
                # Filter only 'bad' statuses
                if event["status"] == "operational":
                    continue

            events.append(event)
    return JSONResponse(content=events, indent=2)
#   return events


