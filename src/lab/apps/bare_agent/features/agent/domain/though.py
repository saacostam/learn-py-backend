from dataclasses import dataclass


@dataclass
class Though:
    id: str
    content: str


@dataclass
class LeanChainOfThough:
    id: str
    chat_id: str
    objective: str


@dataclass
class ChainOfThough(LeanChainOfThough):
    thoughts: list[Though]
