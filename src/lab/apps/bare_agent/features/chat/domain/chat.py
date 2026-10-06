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
class LeanChat:
    id: str
    user_id: str


@dataclass
class Chat(LeanChat):
    turns: list[Turn]
