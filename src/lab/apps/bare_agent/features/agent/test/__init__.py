from unittest.mock import Mock

from lab.apps.bare_agent.features.agent.domain import (
    ChainOfThoughRepository,
)


def mock_chain_of_though_repository():
    return Mock(spec=ChainOfThoughRepository)
