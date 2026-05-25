import redis.asyncio as redis 

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


async def blacklist_token(jti: str, exp: int):
    ''' Blacklists a JWT token by storing its JTI in Redis with an expiration time.
        - jti: The unique identifier of the JWT token to blacklist.
        - exp: The expiration time of the token (in seconds since epoch) to set the Redis key expiration.
        - Stores the JTI in Redis with a value of "true" and sets the key to expire when the token would 
            naturally expire, ensuring efficient cleanup.
    '''
    ttl = exp
    await redis_client.setex(f"bl:{jti}", ttl, "true")
    
    
async def is_blacklisted(jti: str):
    ''' Checks if a JWT token's JTI is blacklisted by looking it up in Redis.
        - jti: The unique identifier of the JWT token to check.
        - Returns True if the JTI is found in Redis (indicating the token is blacklisted), 
            or False if it is not found (indicating the token is not blacklisted).
    '''
    return await redis_client.exists(f"bl:{jti}")