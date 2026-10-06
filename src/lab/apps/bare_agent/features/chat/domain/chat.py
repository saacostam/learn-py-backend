from dataclasses import dataclass
from enum import Enum


class TurnType(Enum):
    ASSISTANT = "ASSISTANT"
    USER = "USER"


@dataclass
class Turn:
    id: str
    type: TurnType
    content: str


@dataclass
class Chat:
    id: str
    turns: Turn
