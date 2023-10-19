from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from src.lib.storage import Storage

router = APIRouter()


@router.post("")
def upload_file(file: UploadFile, storage: Annotated[Storage, Depends(Storage)]):
    is_uploaded, file_key = storage.upload(file.filename, file.file)

    if not is_uploaded:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail={"message": "Could not upload file"}
        )

    return {"filename": file_key}
