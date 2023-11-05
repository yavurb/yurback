from datetime import datetime, timedelta
from typing import Any, Dict

from argon2 import PasswordHasher
from jose import jwt

from src.core.config import settings

ph = PasswordHasher()
SECRET = settings.jwt_secret


def encode_token(data: Dict[str, Any]) -> str:
    data.update({"exp": datetime.utcnow() + timedelta(days=7)})
    encoded_token = jwt.encode(data, SECRET)
    return encoded_token


def hash_password(password) -> str:
    return ph.hash(password)


def verify_password(hash, password) -> bool:
    return ph.verify(hash, password)
