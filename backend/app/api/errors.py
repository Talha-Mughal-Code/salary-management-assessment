from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.schemas.error import ErrorResponse
from app.services.errors import DuplicateEmailError, EmployeeNotFoundError

NOT_FOUND_RESPONSE = {
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorResponse,
        "description": "No employee with this id.",
    }
}
DUPLICATE_EMAIL_RESPONSE = {
    status.HTTP_409_CONFLICT: {
        "model": ErrorResponse,
        "description": "Another employee already uses this email.",
    }
}


def _error(status_code: int, error: Exception) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"detail": str(error)})


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(EmployeeNotFoundError)
    def employee_not_found(_: Request, error: EmployeeNotFoundError) -> JSONResponse:
        return _error(status.HTTP_404_NOT_FOUND, error)

    @app.exception_handler(DuplicateEmailError)
    def duplicate_email(_: Request, error: DuplicateEmailError) -> JSONResponse:
        return _error(status.HTTP_409_CONFLICT, error)
