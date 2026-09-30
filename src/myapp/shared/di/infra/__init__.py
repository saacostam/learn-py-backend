from myapp.features.app import UserUseCases
from myapp.features.infra import MemoryUserRepository

_user_repo = MemoryUserRepository()

user_use_cases = UserUseCases(user_repo=_user_repo)
