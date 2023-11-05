from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session

from src.core.auth import scope
from src.core.auth.deps import check_scopes
from src.crud.post import post as crud
from src.database.deps import get_db
from src.schemas.generics import ResponseAsList
from src.schemas.post import Post, PostCreate, PostUpdate

router = APIRouter()

NOT_FOUND_MESSAGE = "Post not found"


@router.post("", dependencies=[Security(check_scopes, scopes=[scope.CREATE_POST])])
def create_post(post: PostCreate, db: Annotated[Session, Depends(get_db)]) -> Post:
    post_exists = crud.get(db, {"slug": post.slug})

    if post_exists:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, {"message": "Slug must be unique"}
        )

    post_created = crud.create(db, obj_in=post)

    if not post_created:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": "Could not create post."}
        )

    return post_created


@router.get("")
def get_posts(db: Annotated[Session, Depends(get_db)]) -> ResponseAsList[Post]:
    posts = crud.get_multi(db)

    if not posts:
        posts = []

    return ResponseAsList(
        data=posts,
    )


@router.get("/{id}")
def get_post(id: int, db: Annotated[Session, Depends(get_db)]) -> Post:
    post = crud.get_by_id(db, id)

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, {"message": NOT_FOUND_MESSAGE})

    return post


@router.patch(
    "/{id}", dependencies=[Security(check_scopes, scopes=[scope.UPDATE_POST])]
)
def update_post(
    post: PostUpdate, id: int, db: Annotated[Session, Depends(get_db)]
) -> Post:
    db_post = crud.get_by_id(db, id)

    if not db_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, {"message": NOT_FOUND_MESSAGE})

    updated_post = crud.update(db, id=id, obj_in=post)

    if not updated_post:  # TODO: Return exactly why the post couldn't be updated
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": "Could not create post."}
        )

    return updated_post


@router.delete(
    "/{id}",
    status_code=204,
    dependencies=[Security(check_scopes, scopes=[scope.DELETE_POST])],
)
def delete_post(id: int, db: Annotated[Session, Depends(get_db)]) -> None:
    post = crud.get_by_id(db, id)

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, {"message": NOT_FOUND_MESSAGE})

    crud.remove(db, id=id)
    return None
