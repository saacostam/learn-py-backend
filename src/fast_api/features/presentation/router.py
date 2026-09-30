from fastapi import APIRouter

from fast_api.shared.di.infra import user_use_cases

user_router = APIRouter()


@user_router.get("/{user_id}")
def get_user_route(user_id: str):
    return user_use_cases.get_by_id(id=user_id)
