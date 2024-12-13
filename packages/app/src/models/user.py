from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr, Field

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


class User(BaseDocument):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: EmailStr = Field(...)
    addresses: List[Address] = Field(default_factory=list)
    phones: List[Phone] = Field(default_factory=list)
    is_active: bool = Field(default=True)

    model_config = ConfigDict(
        collection_name="users",
        indexes=[
            {"fields": ["email"], "unique": True},
            {"fields": ["created_at"]},
            {"fields": ["is_active"]},
        ],
    )
