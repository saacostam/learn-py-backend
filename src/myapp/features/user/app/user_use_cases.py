from myapp.features.user.domain import User, UserRepository, UserWithPwHash
from myapp.shared.adapters.domain import IdGenerator
from myapp.shared.errors.domain import DomainError, ErrorType


class UserUseCases:
    def __init__(self, id_generator: IdGenerator, user_repo: UserRepository) -> None:
        self.id_generator = id_generator
        self.user_repo = user_repo

    async def create(self, name: str) -> str:
        user = UserWithPwHash(
            id=self.id_generator.gen(),
            name=name,
            pw_hash="REPLACE_ME",
        )

        created_user = await self.user_repo.create(user)

        return created_user.id

    async def get_by_id(self, id: str) -> User:
        user = await self.user_repo.get_by_id(user_id=id)

        if user is None:
            raise DomainError(
                msg=f"User with id '{id}' was not found",
                type=ErrorType.NOT_FOUND,
                user_msg="User not found.",
            )

        return user
