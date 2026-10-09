from datetime import timedelta
from logging import getLogger

from lab.apps.bare_agent.features.agent.app import (
    AgentUseCases,
    AgentWorkerUseCases,
)
from lab.apps.bare_agent.features.agent.domain import (
    ChainOfThoughtRepository,
)
from lab.apps.bare_agent.features.agent.infra import (
    MemoryThoughtRepository,
)
from lab.apps.bare_agent.features.chat.domain import (
    ChatRepository,
)
from lab.apps.bare_agent.features.chat.infra import (
    MemoryChatRepository,
)
from lab.apps.bare_agent.shared.adapters.domain import (
    IdGenerator,
    Logger,
    Queue,
)
from lab.apps.bare_agent.shared.adapters.infra import (
    InMemoryQueue,
    PythonLogger,
    UserSSEEventEmitter,
    UuidGenerator,
)

# Shared
user_sse_event_emitter = UserSSEEventEmitter()
id_generator: IdGenerator = UuidGenerator()
logger: Logger = PythonLogger(logger=getLogger(name="Logger"))
queue: Queue = InMemoryQueue(timeout=timedelta(minutes=5))

# Chat Module
chat_repo: ChatRepository = MemoryChatRepository()

# Agent Module
cot_repo: ChainOfThoughtRepository = MemoryThoughtRepository()
agent_use_cases = AgentUseCases(
    chat_repo=chat_repo,
    cot_repo=cot_repo,
    id_generator=id_generator,
    queue=queue,
)
agent_worker_use_cases = AgentWorkerUseCases(
    chat_repo=chat_repo,
    cot_repo=cot_repo,
    id_generator=id_generator,
    logger=logger,
    queue=queue,
    user_event_emitter=user_sse_event_emitter,
)
