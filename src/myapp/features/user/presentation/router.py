from fastapi import APIRouter
from pydantic import BaseModel

from myapp.shared.di.infra import user_use_cases


user_router = APIRouter()


class CreateUserRequest(BaseModel):
    name: str


@user_router.post("/")
def create_user_route(request: CreateUserRequest) -> str:
    return user_use_cases.create(name=request.name)


@user_router.get("/{user_id}")
def get_user_route(user_id: str):
    return user_use_cases.get_by_id(id=user_id)
