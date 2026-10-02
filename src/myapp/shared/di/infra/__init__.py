from myapp.features.todo.domain import TodoRepository
from myapp.features.todo.infra import MemoryTodoRepository
from myapp.features.user.app import UserUseCases
from myapp.features.user.domain import UserRepository
from myapp.features.user.infra import MemoryUserRepository
from myapp.shared.adapters.domain import IdGenerator
from myapp.shared.adapters.infra import UuidGenerator

id_generator: IdGenerator = UuidGenerator()

todo_repository: TodoRepository = MemoryTodoRepository()
user_repository: UserRepository = MemoryUserRepository()

user_use_cases = UserUseCases(id_generator=id_generator, user_repo=user_repository)
