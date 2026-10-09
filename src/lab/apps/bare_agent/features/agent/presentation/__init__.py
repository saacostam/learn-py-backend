from collections.abc import AsyncIterator
from typing import Annotated, Protocol

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from lab.apps.bare_agent.shared.di.infra import (
    agent_use_cases,
    user_sse_event_emitter,
)

agent_router = APIRouter()


class CreateAgentRequest(BaseModel):
    message: str


class CreateAgentResponse(BaseModel):
    chat_id: str


class EventSubscriber(Protocol):
    def subscribe(self, id: str) -> AsyncIterator[str]: ...


@agent_router.post("/", response_model=CreateAgentResponse)
async def create_agent(
    request: CreateAgentRequest,
) -> CreateAgentResponse:
    result = await agent_use_cases.create(message=request.message)

    return CreateAgentResponse(chat_id=result.chat_id)


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
