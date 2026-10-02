from dataclasses import dataclass
from enum import StrEnum


class UserStatus(StrEnum):
    ACTIVE = "active"
    SUSPENDED = "suspended"


@dataclass
class User:
    id: str
    name: str
    status: UserStatus = UserStatus.ACTIVE
