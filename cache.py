import redis
import json
import hashlib

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

def _hash_logs(logs: list[str]) -> str:
    joined = "|".join(logs)
    return hashlib.sha256(joined.encode()).hexdigest()

def get_cached_aggregation(logs: list[str]):
    key = _hash_logs(logs)
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    return None

def set_cached_aggregation(logs: list[str], aggregated: dict, ttl: int = 300):
    key = _hash_logs(logs)
    redis_client.setex(key, ttl, json.dumps(aggregated))
