from myapp.apps.todo.features.todo.domain import Todo


class MemoryTodoRepository:
    def __init__(self) -> None:
        self._todos: list[Todo] = []

    async def create(self, todo: Todo) -> Todo:
        self._todos.append(todo)
        return todo

    async def get_by_id(self, id: str) -> Todo | None:
        for todo in self._todos:
            if todo.id == id:
                return todo

        return None

    async def remove(self, id: str) -> str:
        self._todos = [todo for todo in self._todos if todo.id != id]
        return id

    async def update(self, id: str, todo: Todo) -> Todo:
        self._todos = [todo if current.id == id else current for current in self._todos]
        return todo
