from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from myapp.features.todo.presentation import todo_router
from myapp.features.user.presentation import user_router
from myapp.shared.errors.domain import DomainError
from myapp.shared.errors.presentation import (
    domain_error_exception_handler,
    generic_exception_handler,
    validation_exception_handler,
)

app = FastAPI()

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(DomainError, domain_error_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(todo_router, prefix="/todos", tags=["todos"])
app.include_router(user_router, prefix="/users", tags=["users"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
