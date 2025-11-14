from fastapi import FastAPI
from pydantic import BaseModel
import redis
import json

app = FastAPI(title="PolyStatus - CSP Ingestor API")

import os
import redis

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "csp_redis"),  # default to your redis service
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

class ProviderCreate(BaseModel):
    name: str
    feed_url: str
    type: str

@app.post("/api/v1/csp/providers", status_code=201)
def add_provider(provider: ProviderCreate):
    """Add a cloud service provider to monitor."""
    data = provider.model_dump()
    r.hset("csp:providers", provider.name, json.dumps(data))
    return {"message": "Provider enregistré avec succès"}
