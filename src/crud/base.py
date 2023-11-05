import logging
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
from pydantic import BaseModel, TypeAdapter, ValidationError
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

        if not row_instance:
            return None

        model_schema = self.__to_schema(self.schema, row_instance)
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

        if not row_instance:
            return None

        model_schema = self.__to_schema(self.schema, row_instance)
        return model_schema if return_schema else row_instance

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> Optional[list[ModelSchemaType]]:
        stmt = select(self.model).offset(skip).limit(limit)
        rows = db.execute(stmt).scalars().all()

        if not rows:
            return None

        return self.__to_schema(list[self.schema], rows)

    def create(
        self, db: Session, *, obj_in: CreateSchemaType
    ) -> Optional[ModelSchemaType]:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return self.__to_schema(self.schema, db_obj)

    def update(
        self,
        db: Session,
        *,
        id: int,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> Optional[ModelSchemaType]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        stmt = update_row(self.model).where(self.model.id == id).values(update_data).returning(self.model)  # type: ignore
        row_instance = db.execute(stmt).scalar()

        if not row_instance:
            return None

        db.commit()

        return self.__to_schema(self.schema, row_instance)

    def remove(self, db: Session, *, id: int) -> None:
        stmt = delete(self.model).where(self.model.id == id)  # type: ignore
        db.execute(stmt)
        db.commit()
        return None

    SchemaType = TypeVar("SchemaType")

    def __to_schema(self, schema: Type[SchemaType], db_data: Any) -> SchemaType | None:
        try:
            return TypeAdapter(schema).validate_python(db_data)
        except ValidationError as e:
            logging.error(e)
            return None
