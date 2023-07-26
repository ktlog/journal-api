from fastapi import APIRouter

from api.notes import router as notes_router
from api.journals import router as journal_router
from api.auth import router as auth_router


router = APIRouter()
router.include_router(auth_router)
router.include_router(journal_router)
router.include_router(notes_router)
