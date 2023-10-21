from datetime import datetime
from typing import Optional, TypedDict

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    email: str
    disabled: Optional[bool] = False


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserOut(BaseModel):
    token: str


class UserSignIn(BaseModel):
    username: str
    password: str


class User(UserBase):
    id: int
    scopes: list[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuerySchema(TypedDict, total=False):
    id: int
    username: str
    emil: str
    disabled: bool
