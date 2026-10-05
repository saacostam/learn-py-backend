from unittest.mock import Mock

from myapp.apps.todo.features.todo.domain import TodoRepository, UserClient


def mock_todo_repository():
    return Mock(spec=TodoRepository)


def mock_user_client():
    return Mock(spec=UserClient)
