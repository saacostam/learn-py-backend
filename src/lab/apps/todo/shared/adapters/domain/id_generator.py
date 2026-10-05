from typing import Protocol


class IdGenerator(Protocol):
    def gen(self) -> str: ...
