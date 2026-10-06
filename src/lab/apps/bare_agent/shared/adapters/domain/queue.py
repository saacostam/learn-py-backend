from dataclasses import dataclass
from typing import Protocol


@dataclass
class QueueEntry:
    id: str


class Queue(Protocol):
    async def add(self, entry: QueueEntry) -> str: ...
    async def peek(self) -> QueueEntry: ...
    async def remove(self, id: str) -> str | None: ...
