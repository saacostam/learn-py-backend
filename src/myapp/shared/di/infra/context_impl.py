from myapp.features.user.domain import UserRepository
from myapp.features.user.infra import MemoryUserRepository
from myapp.shared.di.app import Repositories


class RepositoriesImpl:
    def __init__(self) -> None:
        self.user: UserRepository = MemoryUserRepository()


class ContextImpl:
    def __init__(self) -> None:
        self.repo: Repositories = RepositoriesImpl()
