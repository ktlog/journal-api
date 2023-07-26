from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from services.auth import AuthService, get_current_user
from schemas.auth import CreateUserSchema, Token, UserSchema

router = APIRouter(
    prefix='/auth',
    tags=['Registration/Authentication']
)


@router.post('/sign-up', response_model=Token)
async def sign_up(
        user_data: CreateUserSchema,
        service: AuthService = Depends()
):
    return await service.register_new_user(user_data)


@router.post('/sign-in', response_model=Token)
async def sign_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends()
):
    return await service.authenticate_user(
        form_data.username,
        form_data.password
    )


@router.get('/user', response_model=UserSchema)
async def get_user(user: UserSchema = Depends(get_current_user)):
    return user
