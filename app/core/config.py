from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


database_driver = os.getenv("MYSQLDB_DRIVER")
database_user = os.getenv("MYSQLDB_USER")
database_password = os.getenv("MYSQLDB_PASSWORD")
database_host = os.getenv("MYSQLDB_HOST")
database_port = os.getenv("MYSQLDB_PORT")
database_name = os.getenv("MYSQLDB_NAME")

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI E-commerce"
    DEBUG: bool = True
    # Default DB url for production/dev; tests override with SQLite in-memory
    DATABASE_URL: str = (
            f"{database_driver}://{database_user}:{database_password}@"
            f"{database_host}:{database_port}/{database_name}"
        )
    JWT_SECRET: str = os.getenv('SECRET_KEY')
    JWT_ALGORITHM: str = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

    class Config:
        env_file = ".env"


settings = Settings()