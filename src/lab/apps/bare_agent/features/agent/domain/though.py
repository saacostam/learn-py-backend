from dataclasses import dataclass


@dataclass
class Thought:
    id: str
    content: str


@dataclass
class LeanChainOfThought:
    id: str
    chat_id: str
    objective: str


@dataclass
class ChainOfThought(LeanChainOfThought):
    thoughts: list[Thought]
