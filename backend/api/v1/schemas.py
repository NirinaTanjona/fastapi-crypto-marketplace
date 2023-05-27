from pydantic import BaseModel
from uuid import UUID


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: UUID
    is_active: bool

    class config:
        orm_mode = True