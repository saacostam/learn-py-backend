from dataclasses import dataclass
from typing import Literal, Protocol


@dataclass(frozen=True)
class EventMessage:
    type: Literal["message"] = "message"


EventEmitterPayload = EventMessage


class EventEmitter(Protocol):
    async def send(
        self,
        id: str,
        event: EventEmitterPayload,
    ) -> None: ...
