from fastapi import APIRouter
from ..database import SessionLocal, engine
from .. import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


# @router.post('/users/', response_model=schemas.User)
# def create_user(user: schemas.UserCreate)
