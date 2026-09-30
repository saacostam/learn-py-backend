from myapp.features.domain import UserRepository
from myapp.features.infra import MemoryUserRepository
from myapp.shared.di.app import Repositories


class RepositoriesImpl:
    def __init__(self) -> None:
        self.user: UserRepository = MemoryUserRepository()


class ContextImpl:
    def __init__(self) -> None:
        self.repo: Repositories = RepositoriesImpl()
