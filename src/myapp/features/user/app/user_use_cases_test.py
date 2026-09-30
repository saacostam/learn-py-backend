from typing import cast

import pytest

from myapp.features.user.app.user_use_cases import UserUseCases
from myapp.features.user.domain import User
from myapp.shared.di.app import Context
from myapp.shared.errors.domain import DomainError, ErrorType
from myapp.test import mock_context


def test_get_by_id_returns_user() -> None:
    ctx = mock_context()

    user = User(
        id="user-1",
        name="John Doe",
    )

    ctx.repo.user.get_by_id.return_value = user

    use_cases = UserUseCases(cast(Context, ctx))

    result = use_cases.get_by_id("user-1")

    assert result == user
    ctx.repo.user.get_by_id.assert_called_once_with(user_id="user-1")


def test_get_by_id_raises_not_found() -> None:
    ctx = mock_context()

    ctx.repo.user.get_by_id.return_value = None

    use_cases = UserUseCases(cast(Context, ctx))

    with pytest.raises(DomainError) as error:
        use_cases.get_by_id("user-1")

    assert error.value.type == ErrorType.NOT_FOUND
    assert error.value.user_msg == "User not found."
    assert error.value.msg == "User with id 'user-1' was not found"

    ctx.repo.user.get_by_id.assert_called_once_with(user_id="user-1")
