from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session

from src.core.auth import scope
from src.core.auth.deps import check_scopes
from src.crud.project import project as crud
from src.database.deps import get_db
from src.schemas.generics import ResponseAsList
from src.schemas.project import Project, ProjectCreate, ProjectUpdate

router = APIRouter()

NOT_FOUND_MESSAGE = "Project not found"


@router.post("", dependencies=[Security(check_scopes, scopes=[scope.CREATE_PROJECT])])
def create_project(
    project: ProjectCreate, db: Annotated[Session, Depends(get_db)]
) -> Project:
    created_project = crud.create(db, obj_in=project)

    if not created_project:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            {"message": "Could not create project."},
        )

    return created_project


@router.get("")
def get_projects(db: Annotated[Session, Depends(get_db)]) -> ResponseAsList[Project]:
    projects = crud.get_multi(db)

    if not projects:
        projects = []

    return ResponseAsList(data=projects)


@router.get("/{id}")
def get_project(id: int, db: Annotated[Session, Depends(get_db)]) -> Project:
    project = crud.get_by_id(db, id)

    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, {"message": NOT_FOUND_MESSAGE})

    return project


@router.patch(
    "/{id}", dependencies=[Security(check_scopes, scopes=[scope.UPDATE_PROJECT])]
)
def update_project(
    project: ProjectUpdate, id: int, db: Annotated[Session, Depends(get_db)]
) -> Project:
    db_project = crud.get_by_id(db, id)

    if not db_project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, {"message": NOT_FOUND_MESSAGE})

    updated_project = crud.update(db, id=id, obj_in=project)

    if not updated_project:  # TODO: Return exactly why the post couldn't be updated
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, {"message": "Could not create post."}
        )

    return updated_project


@router.delete(
    "/{id}",
    status_code=204,
    dependencies=[Security(check_scopes, scopes=[scope.DELETE_PROJECT])],
)
def delete_project(id: int, db: Annotated[Session, Depends(get_db)]) -> None:
    project = crud.get_by_id(db, id)

    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, {"message": NOT_FOUND_MESSAGE})

    crud.remove(db, id=id)
    return None
