from myapp.features.user.domain import User
from myapp.shared.di.app import Context
from myapp.shared.errors.domain import DomainError, ErrorType


class UserUseCases:
    def __init__(self, ctx: Context) -> None:
        self._ctx = ctx

    def get_by_id(self, id: str) -> User:
        user = self._ctx.repo.user.get_by_id(user_id=id)

        if user is None:
            raise DomainError(
                msg=f"User with id '{id}' was not found",
                type=ErrorType.NOT_FOUND,
                user_msg="User not found.",
            )

        return user
