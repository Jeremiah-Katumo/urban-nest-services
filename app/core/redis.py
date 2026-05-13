from redis.asyncio import Redis
import os

redis = Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)


async def blacklist_token(jti: str, exp: int):
    ttl = exp - int(__import__("time").time())
    await redis.setex(f"bl:{jti}", ttl, "1")


async def is_blacklisted(jti: str):
    return await redis.exists(f"bl:{jti}") == 1