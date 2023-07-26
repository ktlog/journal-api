import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, EmailStr

from schemas.journals import JournalSchema


class BaseUserSchema(BaseModel):
    email: EmailStr
    name: str


class CreateUserSchema(BaseUserSchema):
    password: str


class UserSchema(BaseUserSchema):
    id: str | uuid.UUID
    created_at: datetime
    # journals: Optional[List[JournalSchema]] = []

    model_config = ConfigDict(
        from_attributes=True
    )


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
