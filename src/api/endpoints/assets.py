from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security, UploadFile, status
from sqlalchemy.orm import Session

from src.core.auth import scope
from src.core.auth.deps import check_scopes
from src.crud.asset import asset as crud
from src.database.deps import get_db
from src.lib.storage import Storage
from src.schemas.asset import AssetOut, CreateAsset

router = APIRouter()


@router.post("", dependencies=[Security(check_scopes, scopes=[scope.ASSET_CREATE])])
def upload_file(
    file: UploadFile,
    db: Annotated[Session, Depends(get_db)],
    storage: Annotated[Storage, Depends(Storage)],
) -> AssetOut:
    filename = "" if not file.filename else file.filename
    is_uploaded, file_key = storage.upload(filename, file.file)

    if not is_uploaded:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail={"message": "Could not upload file"}
        )

    content_type = "" if not file.content_type else file.content_type
    asset = CreateAsset(key=file_key, mimetype=content_type)
    create_asset = crud.create(db, obj_in=asset)

    if not create_asset:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            {"message": "Could not create asset."},
        )

    return AssetOut(id=create_asset.id, filename=file_key)
