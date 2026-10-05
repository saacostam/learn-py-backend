from fastapi import APIRouter, Depends
from pydantic import BaseModel

from myapp.apps.todo.features.todo.domain import Todo
from myapp.apps.todo.shared.adapters.domain import TokenPayload
from myapp.apps.todo.shared.di.infra import get_current_user, todo_use_cases

todo_router = APIRouter()


class CreateTodoRequest(BaseModel):
    name: str


@todo_router.post("/")
async def create_todo_router(
    req: CreateTodoRequest, payload: TokenPayload = Depends(get_current_user)
) -> Todo:
    res = await todo_use_cases.create(name=req.name, user_id=payload.user_id)
    return res
