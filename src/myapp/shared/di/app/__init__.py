from typing import Protocol

from myapp.features.todo.domain import TodoRepository
from myapp.features.user.domain import UserRepository
from myapp.shared.adapters.domain import IdGenerator


class Adapters(Protocol):
    id: IdGenerator


class Repositories(Protocol):
    todo: TodoRepository
    user: UserRepository


class Context(Protocol):
    adapter: Adapters
    repo: Repositories
