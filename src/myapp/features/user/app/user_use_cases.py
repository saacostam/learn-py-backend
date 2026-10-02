from myapp.features.user.domain import User, UserRepository
from myapp.shared.adapters.domain import IdGenerator
from myapp.shared.errors.domain import DomainError, ErrorType


class UserUseCases:
    def __init__(self, id_generator: IdGenerator, user_repo: UserRepository) -> None:
        self.id_generator = id_generator
        self.user_repo = user_repo

    def create(self, name: str) -> str:
        user: User = User(
            id=self.id_generator.gen(),
            name=name,
        )

        created_user = self.user_repo.create(user)

        return created_user.id

    def get_by_id(self, id: str) -> User:
        user = self.user_repo.get_by_id(user_id=id)

        if user is None:
            raise DomainError(
                msg=f"User with id '{id}' was not found",
                type=ErrorType.NOT_FOUND,
                user_msg="User not found.",
            )

        return user
