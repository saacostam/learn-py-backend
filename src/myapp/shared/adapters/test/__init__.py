from unittest.mock import Mock

from myapp.shared.adapters.domain import IdGenerator, PasswordHasher


def mock_id_generator():
    return Mock(spec=IdGenerator)


def mock_password_hasher():
    return Mock(spec=PasswordHasher)
