from dataclasses import dataclass
from enum import StrEnum


class UserStatus(StrEnum):
    ACTIVE = "active"
    SUSPENDED = "suspended"


@dataclass
class _BaseUser:
    id: str
    name: str


@dataclass
class User(_BaseUser):
    status: UserStatus = UserStatus.ACTIVE


@dataclass
class UserWithPwHash(_BaseUser):
    pw_hash: str
    status: UserStatus = UserStatus.ACTIVE
