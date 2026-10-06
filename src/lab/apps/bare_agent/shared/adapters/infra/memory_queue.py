from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from lab.apps.bare_agent.shared.adapters.domain.queue import QueueEntry


@dataclass
class _QueueItem:
    entry: QueueEntry
    peeked_at: datetime | None = None


class InMemoryQueue:
    def __init__(self, timeout: timedelta):
        self._timeout = timeout
        self._items: list[_QueueItem] = []

    async def add(self, entry: QueueEntry) -> str:
        self._items.append(_QueueItem(entry=entry))
        return entry.id

    async def peek(self) -> QueueEntry | None:
        now = datetime.now(UTC)

        for item in self._items:
            if item.peeked_at is None:
                item.peeked_at = now
                return item.entry

            if now - item.peeked_at >= self._timeout:
                item.peeked_at = now
                return item.entry

        return None

    async def remove(self, id: str) -> str | None:
        for index, item in enumerate(self._items):
            if item.entry.id == id:
                self._items.pop(index)
                return id

        return None
