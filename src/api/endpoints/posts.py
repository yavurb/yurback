from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
from database import deps
from schemas import Post, PostCreate

router = APIRouter()


@router.post("/", response_model=Post)
def create_post(post: PostCreate, db: Annotated[Session, Depends(deps.get_db)]) -> Post:
    post_created = crud.post.create(db, obj_in=post)
    return post_created
