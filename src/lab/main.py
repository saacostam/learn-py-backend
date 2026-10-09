from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from lab.apps.bare_agent.shared.presentation import bare_agent_app_router
from lab.apps.todo.shared.presentation import todo_app_router
from lab.shared.errors.domain import DomainError
from lab.shared.errors.presentation import (
    domain_error_exception_handler,
    generic_exception_handler,
    validation_exception_handler,
)

app = FastAPI()

app.include_router(bare_agent_app_router, prefix="/bare-agent", tags=["bare-agent"])
app.include_router(todo_app_router, prefix="/todo", tags=["todo"])

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(DomainError, domain_error_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.get("/")
def read_root():
    return {"ok": True}
