from lab.apps.todo.features.todo.domain import UserStatus
from lab.apps.todo.features.user.app import UserUseCases


class UserModuleClient:
    def __init__(self, user_use_cases: UserUseCases):
        self.user_use_cases = user_use_cases

    async def get_user_status(self, user_id: str) -> UserStatus:
        user = await self.user_use_cases.get_by_id(id=user_id)

        return UserStatus(user.status)
