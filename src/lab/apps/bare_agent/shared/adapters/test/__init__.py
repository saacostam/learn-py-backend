from unittest.mock import Mock

from lab.apps.bare_agent.shared.adapters.domain import (
    IdGenerator,
    LLMProvider,
    Queue,
)


def mock_id_generator():
    return Mock(spec=IdGenerator)


def mock_llm_provider():
    return Mock(spec=LLMProvider)


def mock_queue():
    return Mock(spec=Queue)
