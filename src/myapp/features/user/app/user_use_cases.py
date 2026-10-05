from myapp.features.user.domain import User, UserRepository, UserWithPwHash
from myapp.shared.adapters.domain import IdGenerator, PasswordHasher
from myapp.shared.errors.domain import DomainError, ErrorType


class UserUseCases:
    def __init__(
        self,
        id_generator: IdGenerator,
        password_hasher: PasswordHasher,
        user_repo: UserRepository,
    ) -> None:
        self.id_generator = id_generator
        self.password_hasher = password_hasher
        self.user_repo = user_repo

    async def get_by_id(self, id: str) -> User:
        user = await self.user_repo.get_by_id(user_id=id)

        if user is None:
            raise DomainError(
                msg=f"User with id '{id}' was not found",
                type=ErrorType.NOT_FOUND,
                user_msg="User not found.",
            )

        return user

    async def signup(self, name: str, password: str) -> str:
        pw_hash = self.password_hasher.hash(password=password)

        user = UserWithPwHash(
            id=self.id_generator.gen(),
            name=name,
            pw_hash=pw_hash,
        )

        created_user = await self.user_repo.create(user)

        return created_user.id
