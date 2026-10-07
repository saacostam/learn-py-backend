from unittest.mock import Mock

from lab.apps.bare_agent.features.agent.domain import (
    ChainOfThought,
)


def mock_chain_of_thought_repository():
    return Mock(spec=ChainOfThought)
