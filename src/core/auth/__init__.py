from datetime import datetime, timedelta
from typing import Annotated, Dict

from argon2 import PasswordHasher
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from src.core.config import settings

ph = PasswordHasher()
oauth2_password_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET = settings.jwt_secret
ALGORITHM = "HS256"


def encode_token(data: Dict[str, any]) -> str:
    data.update({"exp": datetime.utcnow() + timedelta(days=7)})
    encoded_token = jwt.encode(data, SECRET)
    return encoded_token


def decode_token(token: Annotated[str, Depends(oauth2_password_scheme)]):
    payload = jwt.decode(token, SECRET, [ALGORITHM])
    return payload


def hash_password(password):
    return ph.hash(password)


def verify_password(hash, password):
    return ph.verify(hash, password)


def get_current_user(payload: Annotated[Dict[str, any], Depends(decode_token)]):
    pass
