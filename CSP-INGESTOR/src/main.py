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
async def refresh_provider(provider: str):
    data = await fetch_provider_data(provider)  # however you get the JSON

    # Normalize the structure
    if isinstance(data, dict) and "components" in data:
        components = data["components"]
    elif isinstance(data, list):
        components = data
    else:
        # fallback for unexpected structures
        components = []

    refreshed_events = []

    for comp in components:
        # Each comp could have different field names depending on provider
        # We try to normalize them
        service_name = comp.get("name") or comp.get("service") or "Unknown Service"
        status = comp.get("status") or "unknown"

        event = {
            "provider": provider,
            "service": service_name,
            "status": status
        }
        # store in Redis or wherever
        store_event(event)
        refreshed_events.append(event)

    return {
        "message": f"Refreshed {len(refreshed_events)} events",
        "events": refreshed_events
    }
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




# -------------------------
# Helper functions
# -------------------------
import httpx

async def fetch_provider_data(provider: str):
    """
    Fetch the JSON feed for the given provider.
    Looks up provider in Redis first to get feed_url.
    """
    feed_json = r.hget("csp:providers", provider.lower())
    if not feed_json:
        raise HTTPException(status_code=404, detail=f"Provider '{provider}' not found")
    
    feed_info = json.loads(feed_json)
    feed_url = feed_info.get("feed_url")
    if not feed_url:
        raise HTTPException(status_code=400, detail=f"No feed URL found for provider '{provider}'")
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(feed_url)
        resp.raise_for_status()
        return resp.json()


def store_event(event: dict):
    """
    Store an event in Redis under key 'csp:events:<provider>'.
    Each provider has its own list.
    """
    provider = event.get("provider", "unknown").lower()
    key = f"csp:events:{provider}"
    # Push as JSON string
    r.rpush(key, json.dumps(event))
