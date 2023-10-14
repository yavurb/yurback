from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.auth import encode_token, hash_password
from src.crud.user import user as crud
from src.database.deps import get_db
from src.schemas.user import UserCreate, UserOut

router = APIRouter()


@router.post("/signup")
def sign_up(user: UserCreate, db: Annotated[Session, Depends(get_db)]) -> UserOut:
    hashed_password = hash_password(user.password)
    user.password = hashed_password

    created_user = crud.create(db, obj_in=user)

    token = encode_token({"username": created_user.username, "id": created_user.id})
    return {**created_user.__dict__, "token": token}
