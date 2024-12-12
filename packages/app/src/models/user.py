from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class User(BaseModel):
    """User model with basic information"""

    id: Optional[str] = Field(default=None, description="User ID")
    email: EmailStr = Field(..., description="User email address")
    name: str = Field(..., description="User full name")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "is_active": True,
            }
        }
    )
