from dataclasses import dataclass


@dataclass
class Todo:
    id: str
    name: str
    completed: bool
    user_id: str
