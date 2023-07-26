import uuid
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException

from schemas.auth import UserSchema
from schemas.journals import JournalSchema, CreateJournalSchema, UpdateJournalSchema
from services.auth import get_current_user
from services.journals import JournalService

router = APIRouter(
    prefix='/api/journals',
    tags=['Journals']
)


@router.get('/{journal_id}', response_model=JournalSchema)
async def get_journal(
        journal_id: uuid.UUID,
        service: JournalService = Depends(),
        user: UserSchema = Depends(get_current_user)
):
    return await service.get(user_id=user.id, pk=journal_id)


@router.get('/', response_model=List[JournalSchema])
async def get_all_journals(
        service: JournalService = Depends(),
        user: UserSchema = Depends(get_current_user)
):
    return await service.get_all(user_id=user.id)


@router.post('/', response_model=JournalSchema, status_code=status.HTTP_201_CREATED)
async def create_journal(
        data: CreateJournalSchema,
        service: JournalService = Depends(),
        user: UserSchema = Depends(get_current_user)
):
    return await service.create(user.id, data)


@router.put('/{journal_id}', response_model=JournalSchema)
async def update_journal(
        journal_id: uuid.UUID,
        data: UpdateJournalSchema,
        service: JournalService = Depends(),
        user: UserSchema = Depends(get_current_user)
):
    journal = await service.update(user.id, journal_id, data)
    if journal is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка обновления данных."
        )
    return journal


@router.delete('/{journal_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_journal(
        journal_id: uuid.UUID,
        service: JournalService = Depends(),
        user: UserSchema = Depends(get_current_user)
):
    return await service.delete(user.id, journal_id)


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_journals(
        service: JournalService = Depends(),
        user: UserSchema = Depends(get_current_user)
):
    return await service.delete_all(user.id)
