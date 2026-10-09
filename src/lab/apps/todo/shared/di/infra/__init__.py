from lab.apps.todo.features.todo.app import TodoUseCases
from lab.apps.todo.features.todo.domain import TodoRepository, UserClient
from lab.apps.todo.features.todo.infra import MemoryTodoRepository, UserModuleClient
from lab.apps.todo.features.user.app import UserUseCases
from lab.apps.todo.features.user.domain import UserRepository
from lab.apps.todo.features.user.infra import MemoryUserRepository
from lab.apps.todo.shared.adapters.domain import (
    IdGenerator,
    JwtAdapter,
    PasswordHasher,
)
from lab.apps.todo.shared.adapters.infra import (
    BcryptPasswordHasher,
    PyJwtAdapter,
    UuidGenerator,
)
from lab.apps.todo.shared.dependencies import AuthDependency

# Shared
jwt_adapter: JwtAdapter = PyJwtAdapter()
id_generator: IdGenerator = UuidGenerator()
password_hasher: PasswordHasher = BcryptPasswordHasher()

# Deps
get_current_user = AuthDependency(jwt_adapter=jwt_adapter)

# User Module
user_repository: UserRepository = MemoryUserRepository()
user_use_cases = UserUseCases(
    jwt_adapter=jwt_adapter,
    id_generator=id_generator,
    password_hasher=password_hasher,
    user_repo=user_repository,
)

# Todo Module
todo_repository: TodoRepository = MemoryTodoRepository()
user_client: UserClient = UserModuleClient(user_use_cases=user_use_cases)
todo_use_cases = TodoUseCases(
    id_generator=id_generator, todo_repo=todo_repository, user_client=user_client
)
