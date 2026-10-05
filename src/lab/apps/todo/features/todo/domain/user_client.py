from enum import StrEnum
from typing import Protocol


class UserStatus(StrEnum):
    ACTIVE = "active"
    SUSPENDED = "suspended"


class UserClient(Protocol):
    async def get_user_status(self, user_id: str) -> UserStatus: ...
