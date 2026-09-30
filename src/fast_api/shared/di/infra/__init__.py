from fast_api.features.app import UserUseCases
from fast_api.features.infra import MemoryUserRepository

_user_repo = MemoryUserRepository()

user_use_cases = UserUseCases(user_repo=_user_repo)
