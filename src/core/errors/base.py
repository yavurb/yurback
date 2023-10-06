from fastapi import HTTPException
from starlette import status


class BaseError(HTTPException):
    """Raise an HTTP 400 Bad Request error

    Args:
        message (str): The message sent to the client
    """

    def __init__(
        self,
        message: str = "",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:
        super().__init__(detail={"message": message}, status_code=status_code)


class BadRequestError(BaseError):
    def __init__(
        self, message: str = "The request contains invalid or missing data."
    ) -> None:
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)


class NotFoundError(BaseError):
    def __init__(self, message: str = "The requested resource does not exist.") -> None:
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)
