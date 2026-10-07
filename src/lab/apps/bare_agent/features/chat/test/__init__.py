from unittest.mock import Mock

from lab.apps.bare_agent.features.chat.domain import (
    ChatRepository,
)


def mock_chat_repository():
    return Mock(spec=ChatRepository)
