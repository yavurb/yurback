from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def http_exception_handler(_: Request, error: HTTPException) -> JSONResponse:
    return JSONResponse(error.detail, status_code=error.status_code)


def validation_exception_handler(
    _: Request, error: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        content={
            "message": "The submitted data is not valid. Check for errors and try again",
            "errors": [
                {"path": e["loc"][1], "message": e["msg"]} for e in error.errors()
            ],
        },
        status_code=422,
    )
