from unittest.mock import Mock

from lab.apps.bare_agent.shared.adapters.domain import (
    IdGenerator,
    Queue,
)


def mock_id_generator():
    return Mock(spec=IdGenerator)


def mock_queue():
    return Mock(spec=Queue)
