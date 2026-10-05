from myapp.features.todo.app import TodoUseCases
from myapp.features.todo.domain import TodoRepository, UserClient
from myapp.features.todo.infra import MemoryTodoRepository, UserModuleClient
from myapp.features.user.app import UserUseCases
from myapp.features.user.domain import UserRepository
from myapp.features.user.infra import MemoryUserRepository
from myapp.shared.adapters.domain import IdGenerator
from myapp.shared.adapters.infra import UuidGenerator

# Shared
id_generator: IdGenerator = UuidGenerator()

# User Module
user_repository: UserRepository = MemoryUserRepository()
user_use_cases = UserUseCases(id_generator=id_generator, user_repo=user_repository)

### Todo User Module
todo_repository: TodoRepository = MemoryTodoRepository()
user_client: UserClient = UserModuleClient(user_use_cases=user_use_cases)
todo_use_cases = TodoUseCases(
    id_generator=id_generator, todo_repo=todo_repository, user_client=user_client
)
