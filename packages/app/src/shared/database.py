from functools import lru_cache
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from ..config import get_app_db_name, get_mongodb_url


class DatabaseSettings:
    def __init__(self):
        self.mongodb_url = get_mongodb_url()
        self.database_name = get_app_db_name()
        self._client: Optional[AsyncIOMotorClient] = None
        self._db: Optional[AsyncIOMotorDatabase] = None

    async def initialize(self):
        """Initialize database connection if not already initialized."""
        if not self._client:
            self._client = AsyncIOMotorClient(self.mongodb_url)
            self._db = self._client[self.database_name]

            # Here we could add database initialization logic
            # like creating indexes defined in our models

    async def close(self):
        """Close database connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

    @property
    def db(self) -> AsyncIOMotorDatabase:
        """Get database instance."""
        if not self._db:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._db

    def __del__(self):
        """Ensure connection is closed on garbage collection."""
        if self._client:
            self._client.close()


@lru_cache()
def get_database_settings() -> DatabaseSettings:
    """Get database settings singleton."""
    return DatabaseSettings()
