from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.auth import encode_token, hash_password
from src.crud.user import user as crud
from src.database.deps import get_db
from src.schemas.user import UserCreate, UserOut, UserSignIn

router = APIRouter()


@router.post("/signup")
def sign_up(user: UserCreate, db: Annotated[Session, Depends(get_db)]) -> UserOut:
    hashed_password = hash_password(user.password)
    user.password = hashed_password

    created_user = crud.create(db, obj_in=user)

    token = encode_token({"id": created_user.id, "username": created_user.username})
    return {"token": token}


@router.post("/signin")
def sign_in(user: UserSignIn, db: Annotated[Session, Depends(get_db)]) -> UserOut:
    found_user = crud.authenticate(db, user.username, user.password)
    if not found_user:
        raise HTTPException(401, detail={"message": "Username or password incorrect"})

    token = encode_token({"id": found_user.id, "username": found_user.username})
    return {"token": token}
