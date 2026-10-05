from myapp.features.user.domain import User, UserWithPwHash


class MemoryUserRepository:
    def __init__(self) -> None:
        self._users: list[UserWithPwHash] = []

    async def create(self, user: UserWithPwHash) -> User:
        self._users.append(user)
        return User(
            id=user.id,
            name=user.name,
            status=user.status,
        )

    async def get_by_id(self, user_id: str) -> User | None:
        for user in self._users:
            if user.id == user_id:
                return User(
                    id=user.id,
                    name=user.name,
                    status=user.status,
                )

        return None

    async def get_by_name(self, name: str) -> UserWithPwHash | None:
        for user in self._users:
            if user.name == name:
                return user

        return None
