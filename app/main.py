from fastapi import FastAPI
from .api import (
    auth_routes, user_routes
)
from .infrastructure.db.database import db

app = FastAPI(root_path="/app/v1")

@app.on_event("startup")
async def startup():
    await db.create_all_tables()

@app.get("/")
def home():
    return {"message": "Welcome to Urban Homes"}

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(user_routes.router, prefix="/users", tags=["User"])
