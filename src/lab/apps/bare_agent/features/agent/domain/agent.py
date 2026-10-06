from dataclasses import dataclass


@dataclass
class Though:
    id: str
    content: str


@dataclass
class ChainOfThough:
    id: str
    thoughts: list[Though]
