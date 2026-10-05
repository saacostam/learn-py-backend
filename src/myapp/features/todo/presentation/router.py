from fastapi import APIRouter, Depends
from pydantic import BaseModel

from myapp.features.todo.domain import Todo
from myapp.shared.adapters.domain import TokenPayload
from myapp.shared.di.infra import get_current_user, todo_use_cases

todo_router = APIRouter()


class CreateTodoRequest(BaseModel):
    name: str


@todo_router.post("/")
async def create_todo_router(
    req: CreateTodoRequest, payload: TokenPayload = Depends(get_current_user)
) -> Todo:
    res = await todo_use_cases.create(name=req.name, user_id=payload.user_id)
    return res
