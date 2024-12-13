from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    """User model with basic information"""

    id: Optional[str] = Field(default=None, description="User ID")
    email: EmailStr = Field(..., description="User email address")
    name: str = Field(..., description="User full name")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    class Config:
        collection_name = "management_users"  # This defines the MongoDB collection name
        indexes = [
            {
                "fields": ["email"],
                "unique": True,
            },  # Ensure email uniqueness at database level
            {"fields": ["created_at"]},  # Index for timestamp-based queries
            {"fields": ["is_active"]},  # Index for active user queries
        ]
