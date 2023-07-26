import uuid
from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy import update

from sqlalchemy.ext.asyncio import AsyncSession

from models.notes import Note
from schemas.notes import CreateNoteSchema, UpdateNoteSchema
from database import get_async_session


class NoteService:

    def __init__(self, async_session: AsyncSession = Depends(get_async_session)):
        self.async_session = async_session

    async def get(self, user_id: uuid.UUID, journal_id: uuid.UUID, note_id: uuid.UUID) -> Note:
        q = await self.async_session.execute(
            select(Note)
            .where(
                Note.user_id == user_id,
                Note.journal_id == journal_id,
                Note.id == note_id
            )
        )
        note = q.scalar_one_or_none()
        if note is None:
            raise HTTPException(status_code=404, detail='Note not found')
        return note

    async def get_all_notes(self, user_id: uuid.UUID, journal_id: uuid.UUID) -> List[Note]:
        notes = (await self.async_session.execute(
            select(Note)
            .where(
                Note.user_id == user_id,
                Note.journal_id == journal_id
            )
        )).scalars().all()
        if notes is None:
            raise HTTPException(status_code=404, detail=f'Notes not found')
        return notes

    async def create(self, user_id: uuid.UUID, journal_id: uuid.UUID, note_data: CreateNoteSchema) -> Note:
        note = Note(
            **note_data.model_dump(),
            user_id=user_id,
            journal_id=journal_id
        )
        self.async_session.add(note)
        await self.async_session.commit()
        return note

    async def update(self, user_id: uuid.UUID, journal_id: uuid.UUID, pk: uuid.UUID, note: UpdateNoteSchema):
        updated_note = (await self.async_session.execute(
            update(Note)
            .where(
                Note.user_id == user_id,
                Note.journal_id == journal_id,
                Note.id == pk
            )
            .values(**note.model_dump(exclude_unset=True))
            .returning(Note)
        )).scalar_one_or_none()
        await self.async_session.commit()
        return updated_note

    async def delete(self, user_id: uuid.UUID, journal_id: uuid.UUID, note_id: uuid.UUID):
        note = await self.get(user_id, journal_id, note_id)
        await self.async_session.delete(note)
        return await self.async_session.commit()

    async def delete_all(self, user_id: uuid.UUID, journal_id: uuid.UUID):
        result = await self.async_session.scalars(
            select(Note)
            .where(
                Note.user_id == user_id,
                Note.journal_id == journal_id
            )
        )
        notes = result.all()
        for note in notes:
            await self.async_session.delete(note)
        await self.async_session.commit()
