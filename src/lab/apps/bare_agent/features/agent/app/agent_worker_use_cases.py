from typing import Literal

from lab.apps.bare_agent.features.agent.domain import (
    ChainOfThoughtRepository,
)
from lab.apps.bare_agent.features.chat.domain import (
    ChatRepository,
    Turn,
    TurnType,
)
from lab.apps.bare_agent.shared.adapters.domain import (
    EventEmitter,
    EventMessage,
    IdGenerator,
    Logger,
    Queue,
    QueueEntry,
)
from lab.shared.errors.domain import DomainError, ErrorType

DecisionType = Literal["response", "tools"]


class AgentWorkerUseCases:
    def __init__(
        self,
        chat_repo: ChatRepository,
        cot_repo: ChainOfThoughtRepository,
        id_generator: IdGenerator,
        logger: Logger,
        queue: Queue,
        user_event_emitter: EventEmitter,
    ):
        self._chat_repo = chat_repo
        self._cot_repo = cot_repo
        self._id_generator = id_generator
        self._logger = logger
        self._queue = queue
        self._user_event_emitter = user_event_emitter

    async def decision(
        self,
        chat_id: str,
        cot_id: str,
    ):
        # TODO: Add decision logic
        decision: DecisionType = "response"

        self._logger.info(f"Worker.decision.{chat_id}.{cot_id} Decision was {decision}")

        next_entry: QueueEntry
        if decision == "response":
            next_entry = QueueEntry(
                id=self._id_generator.gen(),
                chat_id=chat_id,
                cot_id=cot_id,
                type="response",
            )
        else:
            # TODO: Call tools. For now, loop-back
            next_entry = QueueEntry(
                id=self._id_generator.gen(),
                chat_id=chat_id,
                cot_id=cot_id,
                type="decision",
            )

        await self._queue.add(next_entry)

    async def response(
        self,
        chat_id: str,
        cot_id: str,
    ):
        chat = await self._chat_repo.get_by_id(id=chat_id)

        if chat is None:
            raise DomainError(
                msg=f"AgentsWorkUseCases.response Chat with id {chat_id} not found",
                type=ErrorType.NOT_FOUND,
                user_msg="Failed to respond to missing chat",
            )

        # TODO: Call LLM provider to get response
        response = "Lorem Ipsum"
        self._logger.info(f"Worker.response.{chat_id}.{cot_id} Response is {response}")

        chat.turns.append(
            Turn(
                id=self._id_generator.gen(),
                type=TurnType.ASSISTANT,
                content=response,
            )
        )

        await self._user_event_emitter.send(
            id=chat.user_id, event=EventMessage(type="message")
        )
