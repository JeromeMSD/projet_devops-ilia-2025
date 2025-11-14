import os, redis, json
from pydantic import BaseModel

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "csp_redis"),  # service name from docker-compose
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)
