from enum import Enum
from typing import List

from pydantic import BaseModel, EmailStr, Field

from .base import BaseDocument


class Address(BaseModel):
    street: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    state: str = Field(..., min_length=2, max_length=2)
    postal_code: str = Field(..., min_length=5)
    country: str = Field(default="USA")


class PhoneType(str, Enum):
    MOBILE = "mobile"
    HOME = "home"
    WORK = "work"


class Phone(BaseModel):
    number: str = Field(..., pattern=r"^\+?1?\d{9,15}$")
    type: PhoneType = Field(default=PhoneType.MOBILE)
    is_primary: bool = Field(default=False)


class AUser(BaseDocument):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: EmailStr = Field(...)
    addresses: List[Address] = Field(default_factory=list)
    phones: List[Phone] = Field(default_factory=list)
    is_active: bool = Field(default=True)

    class Config:
        collection_name = "users"  # This defines the MongoDB collection name
        indexes = [
            {
                "fields": ["email"],
                "unique": True,
            },  # Ensure email uniqueness at database level
            {"fields": ["created_at"]},  # Index for timestamp-based queries
            {"fields": ["is_active"]},  # Index for active user queries
        ]
