from typing import Optional

from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorClient

from ...config import get_app_db_name, get_mongodb_url
from ...models.auser import AUser


class UserManagement:
    def __init__(self, mongodb_url=None, db_name=None):
        mongodb_url = mongodb_url or get_mongodb_url()
        db_name = db_name or get_app_db_name()
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db = self.client[db_name]
        self.collection = self.db.users

    async def create_user(self, user: AUser) -> AUser:
        user_dict = user.model_dump()
        user_dict.pop("id", None)
        result = await self.collection.insert_one(user_dict)
        user.id = str(result.inserted_id)
        return user

    async def get_user(self, user_id: str) -> Optional[AUser]:
        try:
            user_dict = await self.collection.find_one({"_id": ObjectId(user_id)})
            if user_dict:
                user_dict["id"] = str(user_dict.pop("_id"))
                return AUser(**user_dict)
        except InvalidId:
            pass
        return None
