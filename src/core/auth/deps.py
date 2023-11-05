from typing import Annotated

from argon2 import PasswordHasher
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.config import settings
from src.crud.user import user as user_crud
from src.database.deps import get_db
from src.schemas.user import User

ph = PasswordHasher()
oauth2_password_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET = settings.jwt_secret
ALGORITHM = "HS256"


class TokenPayload(BaseModel):
    id: int
    username: str


def decode_token(
    token: Annotated[str, Depends(oauth2_password_scheme)]
) -> TokenPayload:
    try:
        payload = jwt.decode(token, SECRET, [ALGORITHM])
        return TokenPayload(**payload)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Could not validate credentials"},
        )


def get_current_user(
    payload: Annotated[TokenPayload, Depends(decode_token)],
    db: Annotated[Session, Depends(get_db)],
) -> User | None:
    user = user_crud.get_by_id(db, payload.id)
    return user


def check_scopes(
    user: Annotated[User, Depends(get_current_user)],
    security_scopes: SecurityScopes,
):
    if "*" in user.scopes:
        return user

    for scope in security_scopes.scopes:
        scope_module = scope.split(":")[0]
        for u_scope in user.scopes:
            if u_scope.startswith(scope_module) and u_scope.endswith("*"):
                return user

        if scope not in user.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"message": "Not enough permissions"},
            )

    return user
