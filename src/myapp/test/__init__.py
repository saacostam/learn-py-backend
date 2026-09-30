from unittest.mock import Mock

from myapp.features.domain import UserRepository


class MockContext:
    def __init__(self) -> None:
        self.repo = Mock()
        self.repo.user = Mock(spec=UserRepository)


def mock_context() -> MockContext:
    return MockContext()
