# src/services/dto/user_dto.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, WithJsonSchema
from pydantic_core import CoreSchema, core_schema
from typeid import TypeID


class TypeIDField(TypeID):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: type[TypeID], _handler: WithJsonSchema
    ) -> CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(TypeID),
                    core_schema.no_info_plain_validator_function(TypeID.from_string),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )


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
