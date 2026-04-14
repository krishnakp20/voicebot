import json

import redis

from app.core.config import settings

redis_client = redis.from_url(settings.redis_url, decode_responses=True)


def enqueue_call_job(payload: dict) -> None:
    redis_client.lpush("call_jobs", json.dumps(payload))
