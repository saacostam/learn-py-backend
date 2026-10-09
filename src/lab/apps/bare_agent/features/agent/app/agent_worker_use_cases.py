from typing import Literal

from pydantic import BaseModel

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
    LLMProvider,
    Logger,
    Message,
    MessageRole,
    Queue,
    QueueEntry,
)
from lab.shared.errors.domain import DomainError, ErrorType


class AgentDecision(BaseModel):
    decision: Literal["response", "tools"]


class AgentResponse(BaseModel):
    content: str


class AgentWorkerUseCases:
    def __init__(
        self,
        chat_repo: ChatRepository,
        cot_repo: ChainOfThoughtRepository,
        id_generator: IdGenerator,
        llm: LLMProvider,
        logger: Logger,
        queue: Queue,
        user_event_emitter: EventEmitter,
    ):
        self._chat_repo = chat_repo
        self._cot_repo = cot_repo
        self._id_generator = id_generator
        self._llm = llm
        self._logger = logger
        self._queue = queue
        self._user_event_emitter = user_event_emitter

    async def decision(
        self,
        chat_id: str,
        cot_id: str,
    ) -> None:
        chat = await self._chat_repo.get_by_id(id=chat_id)

        if chat is None:
            raise DomainError(
                msg=f"AgentWorkerUseCases.decision: Chat {chat_id} not found",
                type=ErrorType.NOT_FOUND,
                user_msg="Failed to process missing chat",
            )

        messages = [
            Message(
                role=MessageRole.SYSTEM,
                content=(
                    "Decide whether the user's request can be answered "
                    "directly or requires tools. Choose 'response' for a "
                    "direct answer and 'tools' when tools are necessary."
                ),
            ),
            *[
                Message(
                    role=(
                        MessageRole.USER
                        if turn.type == TurnType.USER
                        else MessageRole.ASSISTANT
                    ),
                    content=turn.content,
                )
                for turn in chat.turns
            ],
        ]

        result = await self._llm.generate(
            messages=messages,
            output_schema=AgentDecision,
        )
        decision = result.decision

        self._logger.info(f"Worker.decision.{chat_id}.{cot_id} Decision was {decision}")

        if decision == "tools":
            # Tool execution is not implemented yet.
            raise NotImplementedError("Tool execution is not implemented")

        else:
            await self._queue.add(
                QueueEntry(
                    id=self._id_generator.gen(),
                    chat_id=chat_id,
                    cot_id=cot_id,
                    type="response",
                )
            )

    async def response(
        self,
        chat_id: str,
        cot_id: str,
    ) -> None:
        chat = await self._chat_repo.get_by_id(id=chat_id)

        if chat is None:
            raise DomainError(
                msg=f"AgentWorkerUseCases.response: Chat {chat_id} not found",
                type=ErrorType.NOT_FOUND,
                user_msg="Failed to respond to missing chat",
            )

        messages = [
            Message(
                role=MessageRole.SYSTEM,
                content="Answer the user's latest message helpfully and accurately.",
            ),
            *[
                Message(
                    role=(
                        MessageRole.USER
                        if turn.type == TurnType.USER
                        else MessageRole.ASSISTANT
                    ),
                    content=turn.content,
                )
                for turn in chat.turns
            ],
        ]

        result = await self._llm.generate(
            messages=messages,
            output_schema=AgentResponse,
        )
        response = result.content

        self._logger.info(f"Worker.response.{chat_id}.{cot_id} Response generated")

        chat.turns.append(
            Turn(
                id=self._id_generator.gen(),
                type=TurnType.ASSISTANT,
                content=response,
            )
        )

        await self._user_event_emitter.send(
            id=chat.user_id,
            event=EventMessage(content=response, type="message"),
        )
