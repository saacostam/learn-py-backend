from fast_api.features.domain import User


class MemoryUserRepository:
    def __init__(self) -> None:
        self._users: list[User] = [
            User(id="1", name="test-user"),
        ]

    def get_by_id(self, user_id: str) -> User | None:
        for user in self._users:
            if user.id == user_id:
                return user

        return None
