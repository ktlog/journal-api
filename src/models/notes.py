from datetime import datetime
import uuid

from sqlalchemy import String, func, UUID
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Note(Base):
    __tablename__ = 'note'
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, insert_default=uuid.uuid4, index=True)
    title: Mapped[str] = mapped_column(String(128), index=True)
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now(), index=True)
    journal_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('journal.id'))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'))
