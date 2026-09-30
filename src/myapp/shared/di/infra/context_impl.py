from myapp.features.user.domain import UserRepository
from myapp.features.user.infra import MemoryUserRepository
from myapp.shared.adapters.domain import IdGenerator
from myapp.shared.adapters.infra import UuidGenerator
from myapp.shared.di.app import Adapters, Repositories


class AdaptersImpl:
    def __init__(self) -> None:
        self.id: IdGenerator = UuidGenerator()


class RepositoriesImpl:
    def __init__(self) -> None:
        self.user: UserRepository = MemoryUserRepository()


class ContextImpl:
    def __init__(self) -> None:
        self.adapter: Adapters = AdaptersImpl()
        self.repo: Repositories = RepositoriesImpl()
