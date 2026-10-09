from collections.abc import AsyncIterator
from typing import Annotated, Protocol

from fastapi import APIRouter, Path, Query
from fastapi.responses import StreamingResponse

from lab.apps.bare_agent.features.chat.domain import Chat
from lab.apps.bare_agent.shared.di.infra import (
    agent_use_cases,
    user_sse_event_emitter,
)

from .schema import (
    CreateAgentRequest,
    CreateAgentResponse,
    GetAgentResponse,
    TurnResponse,
)

agent_router = APIRouter()


class EventSubscriber(Protocol):
    def subscribe(self, id: str) -> AsyncIterator[str]: ...


@agent_router.post("/", response_model=CreateAgentResponse)
async def create_agent(
    request: CreateAgentRequest,
) -> CreateAgentResponse:
    result = await agent_use_cases.create(message=request.message)

    return CreateAgentResponse(chat_id=result.chat_id)


@agent_router.get("/{chat_id}", response_model=GetAgentResponse)
async def get_agent(
    chat_id: Annotated[str, Path()],
) -> GetAgentResponse:
    chat: Chat = await agent_use_cases.get_by_id(chat_id=chat_id)

    return GetAgentResponse(
        id=chat.id,
        user_id=chat.user_id,
        turns=[
            TurnResponse(
                id=turn.id,
                type=turn.type,
                content=turn.content,
            )
            for turn in chat.turns
        ],
    )


@agent_router.get("/events")
async def get_agent_events(
    user_id: Annotated[str, Query()] = "public",
) -> StreamingResponse:
    subscriber: EventSubscriber = user_sse_event_emitter

    return StreamingResponse(
        subscriber.subscribe(user_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
