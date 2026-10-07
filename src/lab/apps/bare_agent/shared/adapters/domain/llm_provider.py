from dataclasses import dataclass
from enum import Enum
from typing import Protocol, TypeVar

from pydantic import BaseModel


class MessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Message:
    role: MessageRole
    content: str


T = TypeVar("T", bound=BaseModel)


class LLMProvider(Protocol):
    async def generate(
        self,
        messages: list[Message],
        output_schema: type[T],
    ) -> T: ...
