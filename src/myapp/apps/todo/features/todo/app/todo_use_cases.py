from myapp.apps.todo.features.todo.domain import (
    Todo,
    TodoRepository,
    UserClient,
    UserStatus,
)
from myapp.apps.todo.shared.adapters.domain import IdGenerator
from myapp.shared.errors.domain import DomainError, ErrorType


class TodoUseCases:
    def __init__(
        self,
        id_generator: IdGenerator,
        todo_repo: TodoRepository,
        user_client: UserClient,
    ) -> None:
        self.id_generator = id_generator
        self.todo_repo = todo_repo
        self.user_client = user_client

    async def create(self, name: str, user_id: str) -> Todo:
        await self._ensure_user_active(user_id, action="create todo")

        todo: Todo = Todo(
            id=self.id_generator.gen(),
            name=name,
            completed=False,
            user_id=user_id,
        )

        return await self.todo_repo.create(todo)

    async def delete(self, id: str, user_id: str) -> str:
        await self._ensure_user_active(user_id, action="delete todo")

        todo = await self._get_owned_todo(id=id, user_id=user_id)
        await self.todo_repo.remove(id=todo.id)

        return todo.id

    async def get_by_id(self, id: str, user_id: str) -> Todo:
        todo = await self._get_owned_todo(id=id, user_id=user_id)

        return todo

    async def update(
        self, id: str, name: str | None, completed: bool | None, user_id: str
    ) -> Todo:
        await self._ensure_user_active(user_id=user_id, action="update todo")

        todo = await self._get_owned_todo(id=id, user_id=user_id)

        new_todo = await self.todo_repo.update(
            id=todo.id,
            todo=Todo(
                id=todo.id,
                name=name if name is not None else todo.name,
                completed=completed if completed is not None else todo.completed,
                user_id=user_id,
            ),
        )

        return new_todo

    async def _ensure_user_active(self, user_id: str, action: str) -> None:
        user_status = await self.user_client.get_user_status(user_id=user_id)

        if user_status == UserStatus.SUSPENDED:
            raise DomainError(
                msg=f"User with id {user_id} can't {action}",
                user_msg="User is suspended",
                type=ErrorType.FORBIDDEN,
            )

    async def _get_owned_todo(self, id: str, user_id: str) -> Todo:
        todo = await self.todo_repo.get_by_id(id=id)

        discrete_not_found_exception = DomainError(
            msg=f"Todo with id {id} for {user_id} not found",
            user_msg="Todo not found",
            type=ErrorType.NOT_FOUND,
        )

        if todo is None or todo.user_id != user_id:
            raise discrete_not_found_exception

        return todo
