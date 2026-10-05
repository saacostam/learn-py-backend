from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from myapp.apps.todo.shared.presentation import todo_app_router
from myapp.shared.errors.domain import DomainError
from myapp.shared.errors.presentation import (
    domain_error_exception_handler,
    generic_exception_handler,
    validation_exception_handler,
)

app = FastAPI()

app.include_router(todo_app_router, prefix="/todo", tags=["todo"])

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(DomainError, domain_error_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.get("/")
def read_root():
    return {"ok": True}
