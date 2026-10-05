from fastapi import APIRouter
from pydantic import BaseModel

from myapp.features.todo.domain import Todo
from myapp.shared.di.infra import todo_use_cases

todo_router = APIRouter()


class CreateTodoRequest(BaseModel):
    name: str
    user_id: str


@todo_router.post("/")
async def create_todo_router(req: CreateTodoRequest) -> Todo:
    res = await todo_use_cases.create(name=req.name, user_id=req.user_id)
    return res
