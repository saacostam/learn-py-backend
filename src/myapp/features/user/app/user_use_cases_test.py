import pytest

from myapp.features.user.app.user_use_cases import UserUseCases
from myapp.features.user.domain import User
from myapp.features.user.test import mock_user_repository
from myapp.shared.adapters.test import mock_id_generator
from myapp.shared.errors.domain import DomainError, ErrorType


def test_create_returns_created_user_id() -> None:
    id_generator = mock_id_generator()
    id_generator.gen.return_value = "user-1"

    created_user = User(
        id="user-1",
        name="John Doe",
    )

    user_repo = mock_user_repository()
    user_repo.create.return_value = created_user

    use_cases = UserUseCases(
        id_generator=id_generator,
        user_repo=user_repo,
    )

    result = use_cases.create("John Doe")

    assert result == "user-1"

    id_generator.gen.assert_called_once_with()
    user_repo.create.assert_called_once_with(
        User(
            id="user-1",
            name="John Doe",
        )
    )


def test_get_by_id_returns_user() -> None:
    id_generator = mock_id_generator()

    user = User(
        id="user-1",
        name="John Doe",
    )

    user_repo = mock_user_repository()
    user_repo.get_by_id.return_value = user

    use_cases = UserUseCases(
        id_generator=id_generator,
        user_repo=user_repo,
    )

    result = use_cases.get_by_id("user-1")

    assert result == user
    user_repo.get_by_id.assert_called_once_with(user_id="user-1")


def test_get_by_id_raises_not_found() -> None:
    id_generator = mock_id_generator()

    user_repo = mock_user_repository()
    user_repo.get_by_id.return_value = None

    use_cases = UserUseCases(
        id_generator=id_generator,
        user_repo=user_repo,
    )

    with pytest.raises(DomainError) as error:
        use_cases.get_by_id("user-1")

    assert error.value.type == ErrorType.NOT_FOUND
    assert error.value.user_msg == "User not found."
    assert error.value.msg == "User with id 'user-1' was not found"

    user_repo.get_by_id.assert_called_once_with(user_id="user-1")
