from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClient

from ..models.base_model import BaseDocument

T = TypeVar("T", bound=BaseDocument)


class BaseRepository(Generic[T]):
    def __init__(self, mongodb_url: str, db_name: str, model_class: type[T]):
        self.client = AsyncIOMotorClient(mongodb_url, uuidRepresentation="standard")
        self.db = self.client[db_name]
        self.model_class = model_class
        self.collection = self.db[model_class.get_collection_name()]

    async def initialize(self):
        for index in self.model_class.get_indexes():
            await self.collection.create_index(index)

    async def create(self, document: T) -> T:
        doc_dict = document.model_dump()
        await self.collection.insert_one(doc_dict)
        return document

    async def get_by_id(self, id: UUID) -> Optional[T]:
        doc = await self.collection.find_one({"id": id})
        return self.model_class(**doc) if doc else None

    async def find_one(self, query: dict) -> Optional[T]:
        doc = await self.collection.find_one(query)
        return self.model_class(**doc) if doc else None

    async def find_many(self, query: dict, skip: int = 0, limit: int = 100) -> List[T]:
        cursor = self.collection.find(query).skip(skip).limit(limit)
        return [self.model_class(**doc) async for doc in cursor]

    async def update(self, id: UUID, update_dict: dict) -> Optional[T]:
        result = await self.collection.find_one_and_update(
            {"id": id}, {"$set": update_dict}, return_document=True
        )
        return self.model_class(**result) if result else None

    async def delete(self, id: UUID) -> bool:
        result = await self.collection.delete_one({"id": id})
        return result.deleted_count > 0
