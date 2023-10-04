from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
from database import deps
from schemas.generics import ResponseAsList
from schemas.post import Post, PostCreate

router = APIRouter()


@router.post("/")
def create_post(post: PostCreate, db: Annotated[Session, Depends(deps.get_db)]) -> Post:
    post_created = crud.post.create(db, obj_in=post)
    return post_created


@router.get("/")
def get_posts(db: Annotated[Session, Depends(deps.get_db)]) -> ResponseAsList[Post]:
    posts = crud.post.get_multi(db)
    return {"data": posts}
