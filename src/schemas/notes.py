from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseNoteSchema(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None


class NoteSchema(BaseNoteSchema):
    id: UUID
    created_at: datetime
    journal_id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )


class CreateNoteSchema(BaseNoteSchema):
    pass


class UpdateNoteSchema(BaseNoteSchema):
    pass
