import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root so 'app' can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import Base
from app.models.models import Base

# Alembic Config
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for autogenerate
target_metadata = Base.metadata


# Build DB URL (FORCE sync driver)
def get_database_url():
    driver = os.getenv("MYSQLDB_DRIVER", "mysql+aiomysql")
    user = os.getenv("MYSQLDB_USER")
    password = os.getenv("MYSQLDB_PASSWORD")
    host = os.getenv("MYSQLDB_HOST", "localhost")
    port = os.getenv("MYSQLDB_PORT", "3306")
    name = os.getenv("MYSQLDB_DB")

    if not name:
        raise ValueError("MYSQLDB_DB is not set")

    url = f"{driver}://{user}:{password}@{host}:{port}/{name}"

    # 🔥 Force sync driver for Alembic
    return url.replace("mysql+aiomysql", "mysql+pymysql")


# OFFLINE MODE
def run_migrations_offline():
    url = get_database_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ONLINE MODE (SYNC — SIMPLE & STABLE)
def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_database_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# Entry point
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()