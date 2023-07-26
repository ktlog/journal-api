import uuid
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException

from schemas.auth import UserSchema
from services.auth import get_current_user
from schemas.notes import CreateNoteSchema, NoteSchema, UpdateNoteSchema
from services.notes import NoteService


router = APIRouter(
    prefix='/api/journals',
    tags=['Notes']
)


@router.get('/{journal_id}/notes/{note_id}', response_model=NoteSchema)
async def get_note(
        journal_id: uuid.UUID,
        note_id: uuid.UUID,
        service: NoteService = Depends(),
        user: UserSchema = Depends(get_current_user)
):
    return await service.get(user.id, journal_id, note_id)


@router.get('/{journal_id}/notes', response_model=List[NoteSchema])
async def get_all_notes(
        journal_id: uuid.UUID,
        service: NoteService = Depends(),
        user: UserSchema = Depends(get_current_user)
):
    return await service.get_all_notes(user.id, journal_id)


@router.post('/{journal_id}/notes', response_model=NoteSchema)
async def create_note(
        journal_id: uuid.UUID,
        data: CreateNoteSchema,
        service: NoteService = Depends(),
        user: UserSchema = Depends(get_current_user)
):
    return await service.create(user.id, journal_id, data)


@router.put('/{journal_id}/notes/{note_id}', response_model=NoteSchema)
async def update_note(
        journal_id: uuid.UUID,
        note_id: uuid.UUID,
        data: UpdateNoteSchema,
        service: NoteService = Depends(),
        user: UserSchema = Depends(get_current_user)
):
    note = await service.update(user.id, journal_id, note_id, data)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка обновления данных"
        )
    return note


@router.delete('/{journal_id}/notes/{note_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
        journal_id: uuid.UUID,
        note_id: uuid.UUID,
        service: NoteService = Depends(),
        user: UserSchema = Depends(get_current_user)
):
    return await service.delete(user.id, journal_id, note_id)


@router.delete('/{journal_id}/notes', status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_notes(
        journal_id: uuid.UUID,
        service: NoteService = Depends(),
        user: UserSchema = Depends(get_current_user)
):
    return await service.delete_all(user.id, journal_id)
