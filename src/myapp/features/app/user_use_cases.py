from myapp.features.domain import User, UserRepository
from myapp.shared.errors.domain import DomainError, ErrorType


class UserUseCases:
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    def get_by_id(self, id: str) -> User:
        user = self._user_repo.get_by_id(user_id=id)

        if user is None:
            raise DomainError(
                msg=f"User with id '{id}' was not found",
                type=ErrorType.NOT_FOUND,
                user_msg="User not found.",
            )

        return user
