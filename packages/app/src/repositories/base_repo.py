from typing import Generic, List, Optional, Type, TypeVar

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from ..models.base import BaseDocument
from ..shared.database import DatabaseSettings, get_database_settings

T = TypeVar("T", bound=BaseDocument)


class BaseRepository(Generic[T]):
    def __init__(
        self, model_class: Type[T], db_settings: Optional[DatabaseSettings] = None
    ):
        self.model_class = model_class
        self._db_settings = db_settings or get_database_settings()
        self._collection: Optional[AsyncIOMotorCollection] = None

    async def initialize(self):
        await self._db_settings.initialize()
        self._collection = self._db_settings.db[
            self.model_class.model_config["collection_name"]
        ]

        if "indexes" in self.model_class.model_config:
            for index in self.model_class.model_config["indexes"]:
                await self._collection.create_index(
                    [(field, 1) for field in index["fields"]],
                    unique=index.get("unique", False),
                )

    async def close(self):
        await self._db_settings.close()

    @property
    def collection(self) -> AsyncIOMotorCollection:
        if not self._collection:
            raise RuntimeError("Repository not initialized. Call initialize() first.")
        return self._collection

    async def find_by_id(self, id: str) -> Optional[T]:
        result = await self.collection.find_one({"_id": ObjectId(id)})
        return self.model_class.model_validate(result) if result else None

    async def find_all(self) -> List[T]:
        cursor = self.collection.find()
        documents = await cursor.to_list(length=None)
        return [self.model_class.model_validate(doc) for doc in documents]

    async def create(self, document: T) -> T:
        result = await self.collection.insert_one(document.dict(by_alias=True))
        return await self.find_by_id(str(result.inserted_id))

    async def update(self, id: str, document: T) -> Optional[T]:
        result = await self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": document.model_dump(exclude={"id"}, exclude_unset=True)},
        )
        if result.modified_count:
            return await self.find_by_id(id)
        return None

    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
