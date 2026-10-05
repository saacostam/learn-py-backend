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
        user = await self.get_by_id_with_pw_hash(user_id=user_id)

        return (
            None
            if user == None
            else User(
                id=user.id,
                name=user.name,
                status=user.status,
            )
        )

    async def get_by_id_with_pw_hash(self, user_id) -> UserWithPwHash | None:
        for user in self._users:
            if user.id == user_id:
                return user

        return None
