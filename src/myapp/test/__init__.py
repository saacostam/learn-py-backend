from unittest.mock import Mock

from myapp.features.user.domain import UserRepository
from myapp.shared.adapters.domain import IdGenerator


class MockContext:
    def __init__(self) -> None:
        self.repo = Mock()
        self.repo.user = Mock(spec=UserRepository)

        self.adapter = Mock()
        self.adapter.id = Mock(spec=IdGenerator)


def mock_context() -> MockContext:
    return MockContext()
