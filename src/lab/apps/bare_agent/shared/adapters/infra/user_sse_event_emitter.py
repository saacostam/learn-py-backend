import asyncio
import json
from collections.abc import AsyncIterator
from dataclasses import asdict

from lab.apps.bare_agent.shared.adapters.domain import (
    EventEmitterPayload,
)


class UserSSEEventEmitter:
    def __init__(self) -> None:
        self._connections: dict[
            str,
            set[asyncio.Queue[EventEmitterPayload]],
        ] = {}
        self._lock = asyncio.Lock()

    async def send(
        self,
        id: str,
        event: EventEmitterPayload,
    ) -> None:
        async with self._lock:
            queues = list(self._connections.get(id, set()))

        for queue in queues:
            await queue.put(event)

    async def subscribe(self, id: str) -> AsyncIterator[str]:
        queue: asyncio.Queue[EventEmitterPayload] = asyncio.Queue()

        async with self._lock:
            self._connections.setdefault(id, set()).add(queue)

        try:
            while True:
                event = await queue.get()
                data = json.dumps(asdict(event))

                yield f"event: {event.type}\ndata: {data}\n\n"
        finally:
            async with self._lock:
                queues = self._connections.get(id)

                if queues is not None:
                    queues.discard(queue)

                    if not queues:
                        del self._connections[id]
