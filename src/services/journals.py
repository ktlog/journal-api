import uuid

from fastapi import Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.journals import CreateJournalSchema, UpdateJournalSchema
from models.journals import Journal
from database import get_async_session


class JournalService:

    def __init__(self, async_session: AsyncSession = Depends(get_async_session)):
        self.async_session = async_session

    async def get(self, user_id: uuid.UUID, pk: uuid.UUID):
        journal = (
            await self.async_session.execute(
                select(Journal)
                .where(Journal.user_id == user_id, Journal.id == pk)
                .options(selectinload(Journal.notes)))
        ).scalar_one_or_none()
        if journal is None:
            raise HTTPException(status_code=404, detail='Journal not found')
        return journal

    async def get_all(self, user_id: uuid.UUID):
        q = await self.async_session.scalars(
            select(Journal)
            .where(Journal.user_id == user_id)
            .options(selectinload(Journal.notes))
        )
        journals = q.all()
        if journals is None:
            raise HTTPException(status_code=404, detail=f'There are no journals yet')
        return journals

    async def create(self, user_id: uuid.UUID, journal_data: CreateJournalSchema) -> Journal:
        journal = Journal(
            **journal_data.model_dump(),
            user_id=user_id,
            notes=[]
        )
        self.async_session.add(journal)
        await self.async_session.commit()
        return journal

    async def update(self, user_id: uuid.UUID, pk: uuid.UUID, journal: UpdateJournalSchema) -> Journal:
        updated_journal = (await self.async_session.execute(
            update(Journal)
            .where(Journal.user_id == user_id, Journal.id == pk)
            .options(selectinload(Journal.notes))
            .values(**journal.model_dump(exclude_unset=True))
            .returning(Journal)
        )).scalar_one_or_none()
        await self.async_session.commit()
        return updated_journal

    async def delete(self, user_id: uuid.UUID, pk: uuid.UUID):
        await self.async_session.delete(await self.get(user_id, pk))
        await self.async_session.commit()

    async def delete_all(self, user_id: uuid.UUID):
        journals = await self.get_all(user_id)
        for journal in journals:
            await self.async_session.delete(journal)
        await self.async_session.commit()
