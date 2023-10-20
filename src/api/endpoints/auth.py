from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session

from src.core.auth import encode_token, hash_password, scope
from src.core.auth.deps import check_scopes
from src.crud.user import user as crud
from src.database.deps import get_db
from src.schemas.user import UserCreate, UserOut, UserSignIn

router = APIRouter()
DBSession = Annotated[Session, Depends(get_db)]


@router.post(
    "/signup",
    dependencies=[Security(check_scopes, scopes=[scope.AUTH_CREATE])],
)
def sign_up(user: UserCreate, db: DBSession) -> UserOut:
    username_exists = crud.get_by_username(db, user.username)
    if username_exists:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": "Username already exists"},
        )

    hashed_password = hash_password(user.password)
    user.password = hashed_password

    created_user = crud.create(db, obj_in=user)

    token = encode_token({"id": created_user.id, "username": created_user.username})
    return {"token": token}


@router.post("/signin")
def sign_in(user: UserSignIn, db: DBSession) -> UserOut:
    found_user = crud.authenticate(db, user.username, user.password)
    if not found_user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Username or password incorrect"},
        )

    token = encode_token({"id": found_user.id, "username": found_user.username})
    return {"token": token}
