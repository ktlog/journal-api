from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from schemas.notes import NoteSchema


class BaseJournalSchema(BaseModel):
    title: str


class JournalSchema(BaseJournalSchema):
    id: UUID
    created_at: datetime
    user_id: UUID
    notes: Optional[List[NoteSchema]] = []

    model_config = ConfigDict(
        from_attributes=True
    )


class CreateJournalSchema(BaseJournalSchema):
    pass


class UpdateJournalSchema(BaseJournalSchema):
    pass
