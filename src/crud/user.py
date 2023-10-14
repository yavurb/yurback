from typing import Optional

from argon2.exceptions import VerifyMismatchError
from sqlalchemy.orm import Session

from src.core.auth import verify_password
from src.crud.base import CRUDBase
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def authenticate(self, db: Session, username, password) -> Optional[User]:
        user = self.get_by_username(db, username)

        if not user:
            return None

        try:
            verify_password(user.password, password)
        except VerifyMismatchError:
            return None

        return user


user = CRUDUser(User)
