import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import Base
from models.journals import Journal


class User(Base):
    __tablename__ = 'user'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, insert_default=uuid.uuid4, index=True)
    email: Mapped[str] = mapped_column(String(32), index=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(32), unique=True)
    password_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False, index=True)

    journals: Mapped[Optional[List['Journal']]] = relationship(
        backref='user',
        cascade='all, delete-orphan'
    )
