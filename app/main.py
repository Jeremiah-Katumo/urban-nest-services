from fastapi import FastAPI
import redis.asyncio as redis
from fastapi.middleware.cors import CORSMiddleware
# from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache import FastAPICache
from .api import (
    auth_routes, user_routes, property_routes, agent_routes, 
    landlord_routes, tenant_routes, transporter_routes,
    permission_routes, role_routes, field_routes, value_routes,
    subscription_routes, 
)
from .infrastructure.db.database import db

app = FastAPI(root_path="/api/v1")

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to Urban Homes"}

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(user_routes.router, prefix="/users", tags=["User"])
app.include_router(landlord_routes.router, prefix="/landlords", tags=["Landlord"])
app.include_router(agent_routes.router, prefix="/agents", tags=["Agent"])
app.include_router(property_routes.router, prefix="/properties", tags=["Property"])
app.include_router(tenant_routes.router, prefix="/tenants", tags=["Tenant"])
app.include_router(transporter_routes.router, prefix="/transporters", tags=["Transporter"])
app.include_router(role_routes.router, prefix="/roles", tags=["Role"])
app.include_router(permission_routes.router, prefix="/permissions", tags=["Permission"])
app.include_router(field_routes.router, prefix="/fields", tags=["Field"])
app.include_router(value_routes.router, prefix="/values", tags=["Value"])
app.include_router(subscription_routes.router, prefix="/subscriptions", tags=["Subscription"])