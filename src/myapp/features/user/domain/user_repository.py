from typing import Protocol

from .user import User


class UserRepository(Protocol):
    async def create(self, user: User) -> User: ...
    async def get_by_id(self, user_id: str) -> User | None: ...
