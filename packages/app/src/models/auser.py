from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class AUser(BaseModel):
    """User model with basic information"""

    id: Optional[str] = Field(default=None, description="User ID")
    email: EmailStr = Field(..., description="User email address")
    name: str = Field(..., description="User full name")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    model_config = ConfigDict(
        collection_name="management_users",
        indexes=[
            {"fields": ["email"], "unique": True},
            {"fields": ["created_at"]},
            {"fields": ["is_active"]},
        ],
    )
