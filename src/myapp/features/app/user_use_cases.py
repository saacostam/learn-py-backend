from myapp.features.domain import User, UserRepository


class UserUseCases:
    _user_repo: UserRepository

    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def get_by_id(self, id: str) -> User:
        user = self._user_repo.get_by_id(id)

        if user is None:
            raise ValueError("User not found")

        return user
