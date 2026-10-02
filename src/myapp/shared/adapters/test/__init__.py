from unittest.mock import Mock

from myapp.shared.adapters.domain import IdGenerator


def mock_id_generator():
    return Mock(spec=IdGenerator)
