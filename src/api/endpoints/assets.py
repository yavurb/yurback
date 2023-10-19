from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from src.crud.asset import asset as crud
from src.database.deps import get_db
from src.lib.storage import Storage
from src.schemas.asset import CreateAsset

router = APIRouter()


@router.post("")
def upload_file(
    file: UploadFile,
    db: Annotated[Session, Depends(get_db)],
    storage: Annotated[Storage, Depends(Storage)],
):  # TODO: add return type
    is_uploaded, file_key = storage.upload(file.filename, file.file)

    if not is_uploaded:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail={"message": "Could not upload file"}
        )

    asset = CreateAsset(key=file_key, mimetype=file.content_type)
    create_asset = crud.create(db, obj_in=asset)

    return {"id": create_asset.id, "filename": file_key}
