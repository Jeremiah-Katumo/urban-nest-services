import json
import hashlib
from fastapi import Request
from ..redis.redis_client import redis_client

FILTER_CACHE_TTL = 600 # 10 minutes

def generate_filter_key(filters: dict):
    filter_string = "&".join(
        f"{k}={v}" for k, v in sorted(filters.items()) if v is not None
    )
    
    hash_key = hashlib.md5(filter_string.encode()).hexdigest()
    
    return f"products:filter:{hash_key}"

async def get_filter_cache(filters: dict):
    key = generate_filter_key(filters)
    
    data = await redis_client.get(key)
    
    if data:
        return json.loads(data)
    
    return None

async def set_filter_cache(filters: dict, result):
    key = generate_filter_key(filters)
    
    await redis_client.setex(
        key,
        FILTER_CACHE_TTL,
        json.dumps(result)
    )
    
def list_cache_key_builder(
    func,
    namespace: str = "",
    request: Request = None,
    *args,
    **kwargs,
):
    query_params = dict(request.query_params)

    sorted_query = "&".join(
        f"{k}={v}" for k, v in sorted(query_params.items())
    )

    raw_key = f"{namespace}:{request.url.path}:{sorted_query}"

    return hashlib.md5(raw_key.encode()).hexdigest()