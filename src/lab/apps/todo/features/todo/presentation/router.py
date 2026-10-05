from fastapi import APIRouter, Depends
from pydantic import BaseModel

from lab.apps.todo.features.todo.domain import Todo
from lab.apps.todo.shared.adapters.domain import TokenPayload
from lab.apps.todo.shared.di.infra import get_current_user, todo_use_cases

todo_router = APIRouter()


class CreateTodoRequest(BaseModel):
    name: str


@todo_router.post("/")
async def create_todo_router(
    req: CreateTodoRequest, payload: TokenPayload = Depends(get_current_user)
) -> Todo:
    res = await todo_use_cases.create(name=req.name, user_id=payload.user_id)
    return res


@todo_router.get("/")
async def get_all_todos_router(
    payload: TokenPayload = Depends(get_current_user),
) -> list[Todo]:
    res = await todo_use_cases.get_all(user_id=payload.user_id)
    return res


@todo_router.get("/{id}")
async def get_todo_by_id_router(
    id: str, payload: TokenPayload = Depends(get_current_user)
) -> Todo:
    res = await todo_use_cases.get_by_id(id=id, user_id=payload.user_id)
    return res


class UpdateTodoRequest(BaseModel):
    name: str | None = None
    completed: bool | None = None


@todo_router.patch("/{id}")
async def update_todo_router(
    id: str,
    req: UpdateTodoRequest,
    payload: TokenPayload = Depends(get_current_user),
) -> Todo:
    res = await todo_use_cases.update(
        id=id,
        name=req.name,
        completed=req.completed,
        user_id=payload.user_id,
    )
    return res


@todo_router.delete("/{id}")
async def delete_todo_router(
    id: str, payload: TokenPayload = Depends(get_current_user)
) -> str:
    res = await todo_use_cases.delete(id=id, user_id=payload.user_id)
    return res
