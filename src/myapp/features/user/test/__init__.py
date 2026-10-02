from unittest.mock import Mock

from myapp.features.user.domain import UserRepository


def mock_user_repository():
    return Mock(spec=UserRepository)
