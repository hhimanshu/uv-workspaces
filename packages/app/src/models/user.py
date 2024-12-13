from pydantic import EmailStr, Field

from .base_model import BaseDocument


class User(BaseDocument):
    name: str = Field(..., min_length=1)
    email: EmailStr

    @classmethod
    def get_collection_name(cls) -> str:
        return "users"

    @classmethod
    def get_indexes(cls) -> list:
        return [[("id", 1)], [("email", 1)], [("created_at", -1)]]
