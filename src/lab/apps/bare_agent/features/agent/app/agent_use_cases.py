from dataclasses import dataclass

from lab.apps.bare_agent.features.agent.domain import (
    ChainOfThought,
    ChainOfThoughtRepository,
)
from lab.apps.bare_agent.features.chat.domain import (
    Chat,
    ChatRepository,
    Turn,
    TurnType,
)
from lab.apps.bare_agent.shared.adapters.domain import (
    IdGenerator,
    Queue,
    QueueEntry,
)


@dataclass
class CreateResult:
    chat_id: str


USER_ID = "public"


class AgentUseCases:
    def __init__(
        self,
        chat_repo: ChatRepository,
        cot_repo: ChainOfThoughtRepository,
        id_generator: IdGenerator,
        queue: Queue,
    ):
        self._chat_repo = chat_repo
        self._cot_repo = cot_repo
        self._id_generator = id_generator
        self._queue = queue

    async def create(self, message: str) -> CreateResult:
        # Create Chat
        chat_to_be_created: Chat = Chat(
            id=self._id_generator.gen(),
            user_id=USER_ID,
            turns=[
                Turn(
                    id=self._id_generator.gen(),
                    type=TurnType.USER,
                    content=message,
                )
            ],
        )

        chat = await self._chat_repo.create(chat=chat_to_be_created)

        # Create CoT
        chain_of_though_to_be_created: ChainOfThought = ChainOfThought(
            id=self._id_generator.gen(),
            chat_id=chat.id,
            objective=f"Answer this message from the user: ${message}",
            thoughts=[],
        )

        cot = await self._cot_repo.create(chain_of_though_to_be_created)

        # Schedule Though Loop
        await self._queue.add(
            QueueEntry(
                id=self._id_generator.gen(),
                chat_id=chat.id,
                cot_id=cot.id,
                type="decision",
            )
        )

        return CreateResult(
            chat_id=chat.id,
        )
