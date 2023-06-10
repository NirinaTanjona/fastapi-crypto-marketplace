from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from src.database import SessionLocal, engine
from src.auth import models
from src.auth import exceptions
from src.auth.contants import SECRET_KEY, ALGORITHM
from src.auth.schemas import TokenData
from src.auth.service import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise exceptions.credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise exceptions.credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise exceptions.credentials_exception
    return user
