from sqlalchemy import BIGINT, TEXT, Column
from sqlalchemy.orm import relationship

from src.db.base_class import Base

from .mixin import TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id = Column(BIGINT, primary_key=True, index=True, unique=True)
    username = Column(TEXT, index=True, unique=True, nullable=False)
    name = Column(TEXT, nullable=False)
    email = Column(TEXT, index=True, unique=True, nullable=False)

    chats = relationship("Chat", back_populates="user")
