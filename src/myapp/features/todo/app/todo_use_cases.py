from myapp.features.todo.domain import Todo, TodoRepository, UserClient, UserStatus
from myapp.shared.adapters.domain import IdGenerator
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
        user_status = await self.user_client.get_user_status(user_id=user_id)

        if user_status == UserStatus.SUSPENDED:
            raise DomainError(
                msg=f"User with id {user_id} can't create todo",
                user_msg="User is suspended",
                type=ErrorType.FORBIDDEN,
            )

        todo: Todo = Todo(
            id=self.id_generator.gen(),
            name=name,
            completed=False,
        )

        created_todo = await self.todo_repo.create(todo)
        return created_todo
