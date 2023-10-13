from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.crud.project import project as crud
from src.database.deps import get_db
from src.schemas.generics import ResponseAsList
from src.schemas.project import Project, ProjectCreate, ProjectUpdate

router = APIRouter()


@router.post("")
def create_project(
    project: ProjectCreate, db: Annotated[Session, Depends(get_db)]
) -> Project:
    created_project = crud.create(db, obj_in=project)
    return created_project


@router.get("")
def get_projects(db: Annotated[Session, Depends(get_db)]) -> ResponseAsList[Project]:
    projects = crud.get_multi(db)
    return {"data": projects}


@router.get("/{id}")
def get_project(id: int, db: Annotated[Session, Depends(get_db)]) -> Project:
    project = crud.get(db, id)
    return project


@router.patch("/{id}")
def update_project(
    project: ProjectUpdate, id: int, db: Annotated[Session, Depends(get_db)]
) -> Project:
    db_project = crud.get(db, id)
    updated_project = crud.update(db, obj_in=project, db_obj=db_project)
    return updated_project


@router.delete("/{id}", status_code=204)
def delete_project(id: int, db: Annotated[Session, Depends(get_db)]) -> None:
    crud.remove(db, id=id)
    return None
