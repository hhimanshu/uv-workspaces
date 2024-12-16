from datetime import UTC, datetime
from typing import Generic, List, Optional, TypeVar

from motor.motor_asyncio import AsyncIOMotorClient
from typeid import TypeID

from models.base_model import BaseDocument

D = TypeVar("D", bound=BaseDocument)


class BaseRepository(Generic[D]):
    def __init__(self, mongodb_url: str, db_name: str, model_class: type[D]):
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db = self.client[db_name]
        self.model_class = model_class
        self.collection = self.db[model_class.get_collection_name()]
        self._initialized = False

    async def initialize(self):
        if not self._initialized:
            for index in self.model_class.get_indexes():
                await self.collection.create_index(index)
            self._initialized = True

    async def create(self, document: D) -> D:
        await self.initialize()  # Ensure initialization
        doc_dict = document.model_dump()
        doc_dict["id"] = str(doc_dict["id"])  # Convert TypeID to string
        await self.collection.insert_one(doc_dict)
        return document

    async def get_by_id(self, id: TypeID) -> Optional[D]:
        await self.initialize()  # Ensure initialization
        doc = await self.collection.find_one(
            {"id": str(id)}
        )  # Convert TypeID to string
        if doc:
            doc["id"] = TypeID.from_string(doc["id"])  # Convert string back to TypeID
        return self.model_class(**doc) if doc else None

    async def find_one(self, query: dict) -> Optional[D]:
        await self.initialize()  # Ensure initialization
        doc = await self.collection.find_one(query)
        if doc and "id" in doc:
            doc["id"] = TypeID.from_string(doc["id"])  # Convert string back to TypeID
        return self.model_class(**doc) if doc else None

    async def find_many(self, query: dict, skip: int = 0, limit: int = 100) -> List[D]:
        await self.initialize()  # Ensure initialization
        cursor = self.collection.find(query).skip(skip).limit(limit)
        results = []
        async for doc in cursor:
            if "id" in doc:
                doc["id"] = TypeID.from_string(
                    doc["id"]
                )  # Convert string back to TypeID
            results.append(self.model_class(**doc))
        return results

    async def update(self, id: TypeID, update_dict: dict) -> Optional[D]:
        await self.initialize()  # Ensure initialization

        update_dict["updated_at"] = datetime.now(UTC)
        result = await self.collection.find_one_and_update(
            {"id": str(id)},
            {"$set": update_dict},
            return_document=True,  # Convert TypeID to string
        )
        if result and "id" in result:
            result["id"] = TypeID.from_string(
                result["id"]
            )  # Convert string back to TypeID
        return self.model_class(**result) if result else None

    async def delete(self, id: TypeID) -> bool:
        await self.initialize()  # Ensure initialization
        result = await self.collection.delete_one(
            {"id": str(id)}
        )  # Convert TypeID to string
        return result.deleted_count > 0
