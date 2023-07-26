import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, func, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from models.base import Base
from models.notes import Note


class Journal(Base):
    __tablename__ = 'journal'
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, insert_default=uuid.uuid4, index=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now(), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'))

    notes: Mapped[Optional[List['Note']]] = relationship(
        backref=backref('journal'),
        cascade='all, delete-orphan'
    )
