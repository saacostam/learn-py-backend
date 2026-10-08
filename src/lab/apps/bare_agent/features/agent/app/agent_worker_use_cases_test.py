from lab.apps.bare_agent.features.agent.test import mock_chain_of_thought_repository
from lab.apps.bare_agent.features.chat.domain import Chat, Turn, TurnType
from lab.apps.bare_agent.features.chat.test import mock_chat_repository
from lab.apps.bare_agent.shared.adapters.domain import EventMessage, QueueEntry
from lab.apps.bare_agent.shared.adapters.test import (
    mock_event_emitter,
    mock_id_generator,
    mock_logger,
    mock_queue,
)
from lab.shared.errors.domain import DomainError, ErrorType

from . import AgentWorkerUseCases


async def test_decision_response_success() -> None:
    id_generator = mock_id_generator()
    id_generator.gen.return_value = "queue-entry-id-123"

    chat_repo = mock_chat_repository()
    cot_repo = mock_chain_of_thought_repository()
    logger = mock_logger()
    queue = mock_queue()
    event_emitter = mock_event_emitter()

    use_cases = AgentWorkerUseCases(
        chat_repo=chat_repo,
        cot_repo=cot_repo,
        id_generator=id_generator,
        logger=logger,
        queue=queue,
        user_event_emitter=event_emitter,
    )

    await use_cases.decision(
        chat_id="chat-id-123",
        cot_id="cot-id-123",
    )

    logger.info.assert_called_once_with(
        "Worker.decision.chat-id-123.cot-id-123 Decision was response"
    )

    queue.add.assert_awaited_once_with(
        QueueEntry(
            id="queue-entry-id-123",
            chat_id="chat-id-123",
            cot_id="cot-id-123",
            type="response",
        )
    )

    id_generator.gen.assert_called_once_with()


async def test_response_success() -> None:
    id_generator = mock_id_generator()
    id_generator.gen.return_value = "turn-id-123"

    existing_chat = Chat(
        id="chat-id-123",
        user_id="public",
        turns=[
            Turn(
                id="user-turn-id-123",
                type=TurnType.USER,
                content="Hello",
            )
        ],
    )

    chat_repo = mock_chat_repository()
    chat_repo.get_by_id.return_value = existing_chat

    cot_repo = mock_chain_of_thought_repository()
    logger = mock_logger()
    queue = mock_queue()
    event_emitter = mock_event_emitter()

    use_cases = AgentWorkerUseCases(
        chat_repo=chat_repo,
        cot_repo=cot_repo,
        id_generator=id_generator,
        logger=logger,
        queue=queue,
        user_event_emitter=event_emitter,
    )

    await use_cases.response(
        chat_id="chat-id-123",
        cot_id="cot-id-123",
    )

    expected_turn = Turn(
        id="turn-id-123",
        type=TurnType.ASSISTANT,
        content="Lorem Ipsum",
    )

    assert existing_chat.turns[-1] == expected_turn

    chat_repo.get_by_id.assert_awaited_once_with(id="chat-id-123")

    logger.info.assert_called_once_with(
        "Worker.response.chat-id-123.cot-id-123 Response is Lorem Ipsum"
    )

    event_emitter.send.assert_awaited_once_with(
        id="public",
        event=EventMessage(type="message"),
    )

    id_generator.gen.assert_called_once_with()


async def test_response_chat_not_found() -> None:
    chat_repo = mock_chat_repository()
    chat_repo.get_by_id.return_value = None

    cot_repo = mock_chain_of_thought_repository()
    id_generator = mock_id_generator()
    logger = mock_logger()
    queue = mock_queue()
    event_emitter = mock_event_emitter()

    use_cases = AgentWorkerUseCases(
        chat_repo=chat_repo,
        cot_repo=cot_repo,
        id_generator=id_generator,
        logger=logger,
        queue=queue,
        user_event_emitter=event_emitter,
    )

    try:
        await use_cases.response(
            chat_id="chat-id-123",
            cot_id="cot-id-123",
        )
        assert False, "Expected DomainError"
    except DomainError as error:
        assert error.type == ErrorType.NOT_FOUND
        assert error.msg == (
            "AgentsWorkUseCases.response Chat with id chat-id-123 not found"
        )
        assert error.user_msg == "Failed to respond to missing chat"

    chat_repo.get_by_id.assert_awaited_once_with(id="chat-id-123")
    id_generator.gen.assert_not_called()
    logger.info.assert_not_called()
    event_emitter.send.assert_not_awaited()
