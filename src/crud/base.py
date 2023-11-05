from typing import (
    Any,
    Dict,
    Generic,
    Literal,
    Optional,
    Type,
    TypedDict,
    TypeVar,
    Union,
    overload,
)

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, TypeAdapter
from sqlalchemy import delete, select
from sqlalchemy import update as update_row
from sqlalchemy.orm import Session

from src.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)
ModelSchemaType = TypeVar("ModelSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
QuerySchemaType = TypeVar("QuerySchemaType", bound=TypedDict)


class CRUDBase(
    Generic[
        ModelType,
        ModelSchemaType,
        CreateSchemaType,
        UpdateSchemaType,
        QuerySchemaType,
    ]
):
    def __init__(self, model: Type[ModelType], schema: Type[ModelSchemaType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.schema = schema

    @overload
    def get_by_id(
        self, db: Session, id: Any, *, return_schema: Literal[True] = True
    ) -> Optional[ModelSchemaType]:
        ...

    @overload
    def get_by_id(
        self, db: Session, id: Any, *, return_schema: Literal[False] = False
    ) -> Optional[ModelType]:
        ...

    def get_by_id(
        self, db: Session, id: Any, *, return_schema: bool = True
    ) -> Optional[ModelSchemaType | ModelType]:
        row_instance = db.get(self.model, id)
        model_schema = TypeAdapter(self.schema).validate_python(row_instance)
        return model_schema if return_schema else row_instance

    @overload
    def get(
        self,
        db: Session,
        query: QuerySchemaType,
        *,
        return_schema: Literal[True] = True,
    ) -> Optional[ModelSchemaType]:
        ...

    @overload
    def get(
        self,
        db: Session,
        query: QuerySchemaType,
        *,
        return_schema: Literal[False] = False,
    ) -> Optional[ModelType]:
        ...

    def get(
        self, db: Session, query: QuerySchemaType, *, return_schema: bool = True
    ) -> Optional[ModelSchemaType | ModelType]:
        stmt = select(self.model).filter_by(**query).limit(1)
        row_instance = db.execute(stmt).scalar()

        model_schema = TypeAdapter(self.schema).validate_python(row_instance)
        return model_schema if return_schema else row_instance

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[ModelSchemaType]:
        stmt = select(self.model).offset(skip).limit(limit)
        rows = db.execute(stmt).scalars().all()

        return TypeAdapter(list[self.schema]).validate_python(rows)

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelSchemaType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return TypeAdapter(self.schema).validate_python(db_obj)

    def update(
        self,
        db: Session,
        *,
        id: int,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelSchemaType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        stmt = update_row(self.model).where(self.model.id == id).values(update_data).returning(self.model)  # type: ignore
        row_instance = db.execute(stmt).scalar()

        db.commit()

        return TypeAdapter(self.schema).validate_python(row_instance)

    def remove(self, db: Session, *, id: int) -> None:
        stmt = delete(self.model).where(self.model.id == id)  # type: ignore
        db.execute(stmt)
        db.commit()
        return None
