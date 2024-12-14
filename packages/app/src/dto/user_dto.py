# src/services/dto/user_dto.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .typeid_field import TypeIDField


class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr


class UpdateUserRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None


class UserResponse(BaseModel):
    id: TypeIDField
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)
