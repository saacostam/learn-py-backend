from fastapi import APIRouter

from lab.apps.todo.features.todo.presentation import todo_router
from lab.apps.todo.features.user.presentation import user_router

todo_app_router = APIRouter()

todo_app_router.include_router(todo_router, prefix="/todos", tags=["todos"])
todo_app_router.include_router(user_router, prefix="/users", tags=["users"])
