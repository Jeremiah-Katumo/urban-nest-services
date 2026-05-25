import json
import hashlib
from fastapi import Request
from ..redis.redis_client import redis_client

FILTER_CACHE_TTL = 600 # 10 minutes

def generate_filter_key(filters: dict):
    ''' Generates a unique cache key for a given set of filters.
        - filters: A dictionary of filter criteria where keys are filter names and values are filter values.
        - Constructs a string representation of the filters by sorting the key-value pairs and joining them with "&".
        - Hashes the resulting string using MD5 to create a unique and consistent cache key.
        - Returns the generated cache key in the format "products:filter:{hash_key}".
    '''
    filter_string = "&".join(
        f"{k}={v}" for k, v in sorted(filters.items()) if v is not None
    )
    
    hash_key = hashlib.md5(filter_string.encode()).hexdigest()
    
    return f"products:filter:{hash_key}"

async def get_filter_cache(filters: dict):
    ''' Retrieves cached results for a given set of filters from Redis.
        - filters: A dictionary of filter criteria where keys are filter names and values are filter values.
        - Generates a cache key using the generate_filter_key function based on the provided filters.
    '''
    key = generate_filter_key(filters)
    
    data = await redis_client.get(key)
    
    if data:
        return json.loads(data)
    
    return None

async def set_filter_cache(filters: dict, result):
    ''' Caches the results of a query for a given set of filters in Redis.
        - filters: A dictionary of filter criteria where keys are filter names and values are filter values.
        - result: The data to be cached, typically the result of a database query based on the filters.
        - Generates a cache key using the generate_filter_key function based on the provided filters.
        - Stores the result in Redis with the generated cache key and sets an expiration time defined by 
            FILTER_CACHE_TTL to ensure that stale data is automatically removed from the cache after a 
            certain period.
    '''
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
    ''' Builds a cache key for list endpoints based on the request path and query parameters.
        - func: The function for which the cache key is being built (not used in this implementation but 
            can be included for extensibility).
        - namespace: A string prefix to categorize the cache key, typically representing the resource 
            type (e.g., "products").
        - request: The FastAPI Request object containing the path and query parameters to be included 
            in the cache key.
        - args and kwargs: Additional arguments that can be used for more complex cache key generation 
            if needed (not used in this implementation).
        - Constructs a cache key by combining the namespace, request path, and sorted query parameters, 
            then hashing the resulting string using MD5 to create a unique and consistent cache key.
    '''
    query_params = dict(request.query_params)

    sorted_query = "&".join(
        f"{k}={v}" for k, v in sorted(query_params.items())
    )

    raw_key = f"{namespace}:{request.url.path}:{sorted_query}"

    return hashlib.md5(raw_key.encode()).hexdigest()