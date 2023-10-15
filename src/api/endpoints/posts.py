from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.crud.post import post as crud
from src.database.deps import get_db
from src.schemas.generics import ResponseAsList
from src.schemas.post import Post, PostCreate, PostUpdate

router = APIRouter()


@router.post("")
def create_post(post: PostCreate, db: Annotated[Session, Depends(get_db)]) -> Post:
    post_created = crud.create(db, obj_in=post)
    return post_created


@router.get("")
def get_posts(db: Annotated[Session, Depends(get_db)]) -> ResponseAsList[Post]:
    posts = crud.post.get_multi(db)
    return {"data": posts}


@router.get("/{id}")
def get_post(id: int, db: Annotated[Session, Depends(get_db)]) -> Post:
    post = crud.get(db, id)
    return post


@router.patch("/{id}")
def update_post(
    post: PostUpdate, id: int, db: Annotated[Session, Depends(get_db)]
) -> Post:
    db_post = crud.post.get(db, id)
    updated_post = crud.update(db, db_obj=db_post, obj_in=post)
    return updated_post


@router.delete("/{id}", status_code=204)
def delete_post(id: int, db: Annotated[Session, Depends(get_db)]) -> None:
    crud.remove(db, id=id)
    return None
