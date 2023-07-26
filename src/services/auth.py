import json
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.auth import User
from schemas.auth import UserSchema, Token, CreateUserSchema
from database import get_async_session
from settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserSchema:
    return await AuthService.validate_token(token)


class AuthService:

    def __init__(self, async_session: AsyncSession = Depends(get_async_session)):
        self.async_session = async_session

    @classmethod
    async def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    async def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    async def validate_token(cls, token: str) -> UserSchema:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials.',
            headers={'WWW-Authenticate': 'Bearer'}
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=settings.jwt_algorithm
            )
        except JWTError:
            raise exception from None

        user_data = json.loads(payload.get('user'))

        try:
            user = UserSchema.model_validate(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    async def create_token(cls, user: User) -> Token:
        user_data = UserSchema.model_validate(user)

        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expiration),
            'sub': str(user_data.id),
            'user': user_data.model_dump_json()
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )

        return Token(access_token=token)

    async def register_new_user(self, user_data: CreateUserSchema) -> Token:
        user = User(
            email=user_data.email,
            name=user_data.name,
            password_hash=await self.hash_password(user_data.password)
        )
        self.async_session.add(user)
        await self.async_session.commit()

        return await self.create_token(user)

    async def authenticate_user(self, username: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password.',
            headers={'WWW-Authenticate': 'Bearer'}
        )

        user = (
            await self.async_session.execute(
                select(User)
                .where(User.name == username))
        ).scalar_one_or_none()

        if not user:
            raise exception

        if not await self.verify_password(password, user.password_hash):
            raise exception

        return await self.create_token(user)
