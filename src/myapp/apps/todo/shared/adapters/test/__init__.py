from unittest.mock import Mock

from myapp.apps.todo.shared.adapters.domain import (
    IdGenerator,
    JwtAdapter,
    PasswordHasher,
)


def mock_jwt_adapter():
    return Mock(spec=JwtAdapter)


def mock_id_generator():
    return Mock(spec=IdGenerator)


def mock_password_hasher():
    return Mock(spec=PasswordHasher)
