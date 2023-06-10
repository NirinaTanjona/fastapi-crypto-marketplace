from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from src.auth.schemas import User, UserCreate, Token
from src.auth.dependencies import get_db
from src.auth.service import get_user_by_mail, authenticate_user, create_user as create_user_service
from src.auth.exceptions import incorrect_credentials
from src.auth.contants import ACCESS_TOKEN_EXPIRE_MINUTES
from src.auth.utils import create_access_token
from src.auth.dependencies import get_current_user

router = APIRouter()


@router.post('/token', response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise incorrect_credentials
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/users/', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_mail(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return create_user_service(db, user)


@router.get('/users/me/', response_model=User)
def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
