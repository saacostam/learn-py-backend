from typing import Protocol

from myapp.features.user.domain import UserRepository
from myapp.shared.adapters.domain import IdGenerator


class Adapters(Protocol):
    id: IdGenerator


class Repositories(Protocol):
    user: UserRepository


class Context(Protocol):
    adapter: Adapters
    repo: Repositories
