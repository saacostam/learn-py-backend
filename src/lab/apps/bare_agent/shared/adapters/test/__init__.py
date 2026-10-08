from unittest.mock import Mock

from lab.apps.bare_agent.shared.adapters.domain import (
    EventEmitter,
    IdGenerator,
    LLMProvider,
    Logger,
    Queue,
)


def mock_event_emitter():
    return Mock(spec=EventEmitter)


def mock_id_generator():
    return Mock(spec=IdGenerator)


def mock_llm_provider():
    return Mock(spec=LLMProvider)


def mock_logger():
    return Mock(spec=Logger)


def mock_queue():
    return Mock(spec=Queue)
