from typing import Protocol

from .user import User


class UserRepository(Protocol):
    def create(self, user: User) -> User: ...
    def get_by_id(self, user_id: str) -> User | None: ...
