from typing import Protocol

from .user import User


class UserRepository(Protocol):
    def get_by_id(self, user_id: str) -> User | None: ...
