import pytest

from myapp.features.user.app.user_use_cases import UserUseCases
from myapp.features.user.domain import User, UserWithPwHash
from myapp.features.user.test import mock_user_repository
from myapp.shared.adapters.test import mock_id_generator, mock_password_hasher
from myapp.shared.errors.domain import DomainError, ErrorType


async def test_create_returns_created_user_id() -> None:
    id_generator = mock_id_generator()
    id_generator.gen.return_value = "user-1"

    password_hasher = mock_password_hasher()
    password_hasher.hash.return_value = "password-hash"

    created_user = User(
        id="user-1",
        name="John Doe",
    )

    user_repo = mock_user_repository()
    user_repo.create.return_value = created_user

    use_cases = UserUseCases(
        id_generator=id_generator,
        password_hasher=password_hasher,
        user_repo=user_repo,
    )

    result = await use_cases.create("John Doe", "password")

    assert result == "user-1"

    id_generator.gen.assert_called_once_with()
    password_hasher.hash.assert_called_once_with(password="password")
    user_repo.create.assert_awaited_once_with(
        UserWithPwHash(
            id="user-1",
            name="John Doe",
            pw_hash="password-hash",
        )
    )


async def test_get_by_id_returns_user() -> None:
    id_generator = mock_id_generator()
    password_hasher = mock_password_hasher()

    user = User(
        id="user-1",
        name="John Doe",
    )

    user_repo = mock_user_repository()
    user_repo.get_by_id.return_value = user

    use_cases = UserUseCases(
        id_generator=id_generator,
        password_hasher=password_hasher,
        user_repo=user_repo,
    )

    result = await use_cases.get_by_id("user-1")

    assert result == user
    user_repo.get_by_id.assert_awaited_once_with(user_id="user-1")


async def test_get_by_id_raises_not_found() -> None:
    id_generator = mock_id_generator()
    password_hasher = mock_password_hasher()

    user_repo = mock_user_repository()
    user_repo.get_by_id.return_value = None

    use_cases = UserUseCases(
        id_generator=id_generator,
        password_hasher=password_hasher,
        user_repo=user_repo,
    )

    with pytest.raises(DomainError) as error:
        await use_cases.get_by_id("user-1")

    assert error.value.type == ErrorType.NOT_FOUND
    assert error.value.user_msg == "User not found."
    assert error.value.msg == "User with id 'user-1' was not found"

    user_repo.get_by_id.assert_awaited_once_with(user_id="user-1")
