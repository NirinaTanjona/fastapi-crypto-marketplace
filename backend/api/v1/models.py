from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
from uuid import uuid4


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid4, unique=True, index=True)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
