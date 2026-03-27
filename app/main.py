from fastapi import FastAPI
import redis.asyncio as redis
# from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache import FastAPICache
from .api import (
    auth_routes, user_routes, property_routes, agent_routes,
    landlord_routes, tenant_routes
)
from .infrastructure.db.database import db

app = FastAPI(root_path="/app/v1")

# Development
@app.on_event("startup")
async def startup():
    await db.create_all_tables()
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
# Production
# @app.on_event("startup")
# async def startup():
#     redis_client = redis.from_url("redis://localhost:6379")
#     FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")

@app.get("/")
def home():
    return {"message": "Welcome to Urban Homes"}

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(user_routes.router, prefix="/users", tags=["User"])
app.include_router(landlord_routes.router, prefix="/landlords", tags=["Landlord"])
app.include_router(agent_routes.router, prefix="/agents", tags=["Agent"])
app.include_router(property_routes.router, prefix="/properties", tags=["Property"])
app.include_router(tenant_routes.router, prefix="/tenants", tags=["Tenant"])
