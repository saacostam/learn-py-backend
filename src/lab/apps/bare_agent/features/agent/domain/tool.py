from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class Tool[T: BaseModel]:
    name: str
    description: str
    input_schema: type[T]
    execute: Callable[[T], Awaitable[object]]
