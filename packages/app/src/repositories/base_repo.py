from typing import Generic, List, Optional, Type, TypeVar

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from shared.database import get_database_settings

from ..models.base import BaseDocument

T = TypeVar("T", bound=BaseDocument)


class BaseRepository(Generic[T]):
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
        self._collection: Optional[AsyncIOMotorCollection] = None

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """Get the MongoDB collection, initializing it if necessary."""
        if not self._collection:
            db_settings = get_database_settings()
            collection_name = self.model_class.Config.collection_name
            self._collection = db_settings.db[collection_name]

            # Create indexes if they're defined in the model
            if hasattr(self.model_class.Config, "indexes"):
                for index in self.model_class.Config.indexes:
                    self._collection.create_index(
                        [(field, 1) for field in index["fields"]],
                        unique=index.get("unique", False),
                    )

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
