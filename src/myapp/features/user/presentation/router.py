from fastapi import APIRouter
from pydantic import BaseModel

from myapp.shared.di.infra import user_use_cases

user_router = APIRouter()


class CreateUserRequest(BaseModel):
    name: str
    password: str


@user_router.post("/")
async def signup_user_route(request: CreateUserRequest) -> str:
    res = await user_use_cases.signup(name=request.name, password=request.password)
    return res


@user_router.get("/{user_id}")
async def get_user_route(user_id: str):
    return user_use_cases.get_by_id(id=user_id)
