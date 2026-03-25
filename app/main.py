from fastapi import FastAPI
from .api import user_routes

app = FastAPI(root_path="/app/v1")

@app.get("/")
def home():
    return {"message": "Welcome to Urban Homes"}

app.include_router(user_routes.router, prefix="/users", tags=["User"])
