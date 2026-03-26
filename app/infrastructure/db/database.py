from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlmodel import SQLModel
from typing import AsyncGenerator
from dotenv import load_dotenv
from threading import Lock
import os

load_dotenv()


class AsyncDatabaseSession:
    _instance = None
    _lock = Lock()

    # def __new__(cls):
    #     if cls._instance is None:
    #         with cls._lock:
    #             if cls._instance is None:
    #                 cls._instance = super().__new__(cls)
    #                 cls._instance.get_engine()
    #     return cls._instance
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AsyncDatabaseSession, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        driver = os.getenv("MYSQLDB_DRIVER")  # e.g., "mysql+aiomysql"
        user = os.getenv("MYSQLDB_USER")
        password = os.getenv("MYSQLDB_PASSWORD")
        host = os.getenv("MYSQLDB_HOST")
        port = os.getenv("MYSQLDB_PORT")
        name = os.getenv("MYSQLDB_DB")
        
        self.db_url = "mysql+aiomysql://jeremy:Mysql.003@localhost:3306/urban_homes"
        
        self.database_url = f"{driver}://{user}:{password}@{host}:{port}/{name}"

        self.engine = create_async_engine(
            self.db_url,
            echo=False,
            pool_pre_ping=True,
        )
        
        self.engine = create_async_engine(
            self.db_url,
            echo=True,
            future=True,
            pool_size=10,
            max_overflow=20,
        )

        self.SessionLocal = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        self.Base = declarative_base()

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.SessionLocal() as session:
            try:
                yield session
                # await session.commit()
            except Exception:
                await session.rollback()
                raise
            
    # Create all tables
    async def create_all_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)

    # Helper to get a single session (useful for scripts)
    @staticmethod
    async def get_session():
        async with AsyncDatabaseSession().SessionLocal() as session:
            
            yield session

    async def get_engine(self):
        '''Engine'''
        return self.engine
    
    async def base(self):
        return self.Base


db = AsyncDatabaseSession()


async def commit_rollback(session: AsyncSession):
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise