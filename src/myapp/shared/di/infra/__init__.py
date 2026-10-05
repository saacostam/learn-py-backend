from myapp.features.todo.app import TodoUseCases
from myapp.features.todo.domain import TodoRepository, UserClient
from myapp.features.todo.infra import MemoryTodoRepository, UserModuleClient
from myapp.features.user.app import UserUseCases
from myapp.features.user.domain import UserRepository
from myapp.features.user.infra import MemoryUserRepository
from myapp.shared.adapters.domain import IdGenerator, JwtAdapter, PasswordHasher
from myapp.shared.adapters.infra import (
    BcryptPasswordHasher,
    PyJwtAdapter,
    UuidGenerator,
)
from myapp.shared.dependencies import AuthDependency

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

### Todo User Module
todo_repository: TodoRepository = MemoryTodoRepository()
user_client: UserClient = UserModuleClient(user_use_cases=user_use_cases)
todo_use_cases = TodoUseCases(
    id_generator=id_generator, todo_repo=todo_repository, user_client=user_client
)
