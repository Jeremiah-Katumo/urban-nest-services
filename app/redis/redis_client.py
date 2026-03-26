import redis.asyncio as redis 

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

async def blacklist_token(jti: str, exp: int):
    ttl = exp
    await redis_client.setex(f"bl:{jti}", ttl, "true")
    
async def is_blacklisted(jti: str):
    return await redis_client.exists(f"bl:{jti}")