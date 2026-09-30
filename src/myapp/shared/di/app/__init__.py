from typing import Protocol

from myapp.features.domain import UserRepository


class Repositories(Protocol):
    user: UserRepository


class Context(Protocol):
    repo: Repositories
