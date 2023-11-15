import logging
from typing import BinaryIO
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError

from src.core.config import settings


class Storage:
    def __init__(self) -> None:
        """
        Storage object to upload binaries to a object storage in the cloud.
        """
        self.__bucket_name = settings.aws_s3_bucket
        self.__storage_client = boto3.resource(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
        self.__bucket = self.__storage_client.Bucket(self.__bucket_name)  # type: ignore

    def upload(self, filename: str, file: BinaryIO) -> tuple[bool, str]:
        filename = self.__append_uid(filename)
        try:
            self.__bucket.upload_fileobj(file, f"assets/{filename}")
        except ClientError as error:
            logging.error(error)
            return (False, filename)

        return (True, filename)

    def __append_uid(self, filename: str) -> str:
        uuid = str(uuid4())
        name = filename.split(".")[0]
        extension = filename.split(".")[-1]
        return f"{name}-{uuid}.{extension}"
