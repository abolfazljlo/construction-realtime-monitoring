from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .base import ResourceInterface
from ..config.database import DatabaseConfig
from ..utils.log import Log
from ..models.db.base import Base

# -------------------------------------------------------------
# Database Manager
# -------------------------------------------------------------
class DatabaseResource(ResourceInterface[DatabaseConfig]):

    def __init__(self, settings):
        super().__init__(settings)
        self.engine = None
        self.session_factory = None

    async def initialize(self):
        self.engine = create_async_engine(
            self.settings.url,
            echo=False,
            future=True
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=True
        )
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
        Log.info("[DatabaseResource] initialized successfully.")

    async def close(self):
        if self.engine:
            await self.engine.dispose()
            Log.info("[DatabaseResource] database engine disposed successfully.")

    @asynccontextmanager
    async def get_session(self):
        async with self.session_factory() as session:
            yield session
