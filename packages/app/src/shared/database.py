from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from config import get_app_db_name, get_mongodb_url


class DatabaseSettings:
    def __init__(
        self, mongodb_url: Optional[str] = None, db_name: Optional[str] = None
    ):
        self.mongodb_url = mongodb_url or get_mongodb_url()
        self.database_name = db_name or get_app_db_name()
        self._client: Optional[AsyncIOMotorClient] = None
        self._db: Optional[AsyncIOMotorDatabase] = None

    async def initialize(self):
        if self._client is None:
            self._client = AsyncIOMotorClient(self.mongodb_url)
            self._db = self._client[self.database_name]

    async def close(self):
        if self._client is not None:
            self._client.close()
            self._client = None
            self._db = None

    @property
    def db(self) -> AsyncIOMotorDatabase:
        if self._db is None:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._db

    def __del__(self):
        if self._client is not None:
            self._client.close()


_instance: Optional[DatabaseSettings] = None


def get_database_settings(
    mongodb_url: Optional[str] = None, db_name: Optional[str] = None
) -> DatabaseSettings:
    """Get database settings instance."""
    global _instance
    if mongodb_url is None and db_name is None:
        if _instance is None:
            _instance = DatabaseSettings()
        return _instance
    else:
        return DatabaseSettings(mongodb_url, db_name)
