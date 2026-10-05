import pytest

from myapp.apps.todo.features.todo.domain import Todo, UserStatus
from myapp.apps.todo.features.todo.test import mock_todo_repository, mock_user_client
from myapp.apps.todo.shared.adapters.test import mock_id_generator
from myapp.shared.errors.domain import DomainError, ErrorType

from . import TodoUseCases


async def test_create_todo_success() -> None:
    id_generator = mock_id_generator()
    id_generator.gen.return_value = "todo-id-123"

    todo_repo = mock_todo_repository()
    created_todo = Todo(
        id="todo-id-123",
        name="Buy groceries",
        completed=False,
        user_id="user-1",
    )
    todo_repo.create.return_value = created_todo

    user_client = mock_user_client()
    user_client.get_user_status.return_value = UserStatus.ACTIVE

    use_cases = TodoUseCases(
        id_generator=id_generator,
        todo_repo=todo_repo,
        user_client=user_client,
    )

    result = await use_cases.create(name="Buy groceries", user_id="user-1")

    assert result == created_todo
    user_client.get_user_status.assert_awaited_once_with(user_id="user-1")
    id_generator.gen.assert_called_once_with()
    todo_repo.create.assert_awaited_once_with(created_todo)


async def test_create_todo_suspended_user_fails() -> None:
    id_generator = mock_id_generator()
    todo_repo = mock_todo_repository()

    user_client = mock_user_client()
    user_client.get_user_status.return_value = UserStatus.SUSPENDED

    use_cases = TodoUseCases(
        id_generator=id_generator,
        todo_repo=todo_repo,
        user_client=user_client,
    )

    with pytest.raises(DomainError) as error:
        await use_cases.create(name="Buy groceries", user_id="user-1")

    assert error.value.type == ErrorType.FORBIDDEN
    assert error.value.user_msg == "User is suspended"

    user_client.get_user_status.assert_awaited_once_with(user_id="user-1")
    id_generator.gen.assert_not_called()
    todo_repo.create.assert_not_awaited()


async def test_delete_todo_success() -> None:
    id_generator = mock_id_generator()

    todo_repo = mock_todo_repository()
    existing_todo = Todo(
        id="todo-id-123",
        name="Buy groceries",
        completed=False,
        user_id="user-1",
    )
    todo_repo.get_by_id.return_value = existing_todo

    user_client = mock_user_client()
    user_client.get_user_status.return_value = UserStatus.ACTIVE

    use_cases = TodoUseCases(
        id_generator=id_generator,
        todo_repo=todo_repo,
        user_client=user_client,
    )

    deleted_id = await use_cases.delete(id="todo-id-123", user_id="user-1")

    assert deleted_id == "todo-id-123"
    user_client.get_user_status.assert_awaited_once_with(user_id="user-1")
    todo_repo.get_by_id.assert_awaited_once_with(id="todo-id-123")
    todo_repo.remove.assert_awaited_once_with(id="todo-id-123")


async def test_delete_todo_suspended_user_fails() -> None:
    id_generator = mock_id_generator()
    todo_repo = mock_todo_repository()

    user_client = mock_user_client()
    user_client.get_user_status.return_value = UserStatus.SUSPENDED

    use_cases = TodoUseCases(
        id_generator=id_generator,
        todo_repo=todo_repo,
        user_client=user_client,
    )

    with pytest.raises(DomainError) as error:
        await use_cases.delete(id="todo-id-123", user_id="user-1")

    assert error.value.type == ErrorType.FORBIDDEN
    assert error.value.user_msg == "User is suspended"

    user_client.get_user_status.assert_awaited_once_with(user_id="user-1")
    todo_repo.get_by_id.assert_not_awaited()
    todo_repo.remove.assert_not_awaited()


async def test_delete_todo_not_found_fails() -> None:
    id_generator = mock_id_generator()

    todo_repo = mock_todo_repository()
    todo_repo.get_by_id.return_value = None

    user_client = mock_user_client()
    user_client.get_user_status.return_value = UserStatus.ACTIVE

    use_cases = TodoUseCases(
        id_generator=id_generator,
        todo_repo=todo_repo,
        user_client=user_client,
    )

    with pytest.raises(DomainError) as error:
        await use_cases.delete(id="non-existent-id", user_id="user-1")

    assert error.value.type == ErrorType.NOT_FOUND
    assert error.value.user_msg == "Todo not found"
    assert error.value.msg == "Todo with id non-existent-id for user-1 not found"

    user_client.get_user_status.assert_awaited_once_with(user_id="user-1")
    todo_repo.get_by_id.assert_awaited_once_with(id="non-existent-id")
    todo_repo.remove.assert_not_awaited()


async def test_delete_todo_wrong_owner_fails() -> None:
    id_generator = mock_id_generator()

    todo_repo = mock_todo_repository()
    foreign_todo = Todo(
        id="todo-id-123",
        name="Buy groceries",
        completed=False,
        user_id="user-2",
    )
    todo_repo.get_by_id.return_value = foreign_todo

    user_client = mock_user_client()
    user_client.get_user_status.return_value = UserStatus.ACTIVE

    use_cases = TodoUseCases(
        id_generator=id_generator,
        todo_repo=todo_repo,
        user_client=user_client,
    )

    with pytest.raises(DomainError) as error:
        await use_cases.delete(id="todo-id-123", user_id="user-1")

    assert error.value.type == ErrorType.NOT_FOUND
    assert error.value.user_msg == "Todo not found"

    user_client.get_user_status.assert_awaited_once_with(user_id="user-1")
    todo_repo.get_by_id.assert_awaited_once_with(id="todo-id-123")
    todo_repo.remove.assert_not_awaited()


async def test_get_todo_by_id_success() -> None:
    id_generator = mock_id_generator()

    todo_repo = mock_todo_repository()
    existing_todo = Todo(
        id="todo-id-123",
        name="Buy groceries",
        completed=False,
        user_id="user-1",
    )
    todo_repo.get_by_id.return_value = existing_todo

    user_client = mock_user_client()
    user_client.get_user_status.return_value = UserStatus.ACTIVE

    use_cases = TodoUseCases(
        id_generator=id_generator,
        todo_repo=todo_repo,
        user_client=user_client,
    )

    result = await use_cases.get_by_id(id="todo-id-123", user_id="user-1")

    assert result == existing_todo
    todo_repo.get_by_id.assert_awaited_once_with(id="todo-id-123")


async def test_get_todo_by_id_not_found_fails() -> None:
    id_generator = mock_id_generator()

    todo_repo = mock_todo_repository()
    todo_repo.get_by_id.return_value = None

    user_client = mock_user_client()
    user_client.get_user_status.return_value = UserStatus.ACTIVE

    use_cases = TodoUseCases(
        id_generator=id_generator,
        todo_repo=todo_repo,
        user_client=user_client,
    )

    with pytest.raises(DomainError) as error:
        await use_cases.get_by_id(id="non-existent-id", user_id="user-1")

    assert error.value.type == ErrorType.NOT_FOUND
    assert error.value.user_msg == "Todo not found"
    assert error.value.msg == "Todo with id non-existent-id for user-1 not found"

    todo_repo.get_by_id.assert_awaited_once_with(id="non-existent-id")


async def test_get_todo_by_id_wrong_owner_fails() -> None:
    id_generator = mock_id_generator()

    todo_repo = mock_todo_repository()
    foreign_todo = Todo(
        id="todo-id-123",
        name="Buy groceries",
        completed=False,
        user_id="user-2",
    )
    todo_repo.get_by_id.return_value = foreign_todo

    user_client = mock_user_client()
    user_client.get_user_status.return_value = UserStatus.ACTIVE

    use_cases = TodoUseCases(
        id_generator=id_generator,
        todo_repo=todo_repo,
        user_client=user_client,
    )

    with pytest.raises(DomainError) as error:
        await use_cases.get_by_id(id="todo-id-123", user_id="user-1")

    assert error.value.type == ErrorType.NOT_FOUND
    assert error.value.user_msg == "Todo not found"

    todo_repo.get_by_id.assert_awaited_once_with(id="todo-id-123")


async def test_update_todo_success() -> None:
    id_generator = mock_id_generator()

    todo_repo = mock_todo_repository()
    existing_todo = Todo(
        id="todo-id-123",
        name="Buy groceries",
        completed=False,
        user_id="user-1",
    )
    todo_repo.get_by_id.return_value = existing_todo

    updated_todo = Todo(
        id="todo-id-123",
        name="Buy organic groceries",
        completed=True,
        user_id="user-1",
    )
    todo_repo.update.return_value = updated_todo

    user_client = mock_user_client()
    user_client.get_user_status.return_value = UserStatus.ACTIVE

    use_cases = TodoUseCases(
        id_generator=id_generator,
        todo_repo=todo_repo,
        user_client=user_client,
    )

    result = await use_cases.update(
        id="todo-id-123",
        name="Buy organic groceries",
        completed=True,
        user_id="user-1",
    )

    assert result == updated_todo
    user_client.get_user_status.assert_awaited_once_with(user_id="user-1")
    todo_repo.get_by_id.assert_awaited_once_with(id="todo-id-123")
    todo_repo.update.assert_awaited_once_with(
        id="todo-id-123",
        todo=updated_todo,
    )


async def test_update_todo_partial_name_only_success() -> None:
    id_generator = mock_id_generator()
    todo_repo = mock_todo_repository()

    existing_todo = Todo(
        id="todo-id-123",
        name="Buy groceries",
        completed=False,
        user_id="user-1",
    )
    todo_repo.get_by_id.return_value = existing_todo

    # Expected result: name changes, completed stays False
    expected_updated_todo = Todo(
        id="todo-id-123",
        name="Buy organic groceries",
        completed=False,
        user_id="user-1",
    )
    todo_repo.update.return_value = expected_updated_todo

    user_client = mock_user_client()
    user_client.get_user_status.return_value = UserStatus.ACTIVE

    use_cases = TodoUseCases(
        id_generator=id_generator,
        todo_repo=todo_repo,
        user_client=user_client,
    )

    result = await use_cases.update(
        id="todo-id-123",
        name="Buy organic groceries",
        completed=None,
        user_id="user-1",
    )

    assert result == expected_updated_todo
    user_client.get_user_status.assert_awaited_once_with(user_id="user-1")
    todo_repo.get_by_id.assert_awaited_once_with(id="todo-id-123")
    todo_repo.update.assert_awaited_once_with(
        id="todo-id-123",
        todo=expected_updated_todo,
    )


async def test_update_todo_partial_completed_to_false_success() -> None:
    id_generator = mock_id_generator()
    todo_repo = mock_todo_repository()

    existing_todo = Todo(
        id="todo-id-123",
        name="Buy groceries",
        completed=True,  # Currently true
        user_id="user-1",
    )
    todo_repo.get_by_id.return_value = existing_todo

    # Expected result: name stays the same, completed updates to False
    expected_updated_todo = Todo(
        id="todo-id-123",
        name="Buy groceries",
        completed=False,
        user_id="user-1",
    )
    todo_repo.update.return_value = expected_updated_todo

    user_client = mock_user_client()
    user_client.get_user_status.return_value = UserStatus.ACTIVE

    use_cases = TodoUseCases(
        id_generator=id_generator,
        todo_repo=todo_repo,
        user_client=user_client,
    )

    result = await use_cases.update(
        id="todo-id-123",
        name=None,
        completed=False,  # Explicitly toggling back to False
        user_id="user-1",
    )

    assert result == expected_updated_todo
    todo_repo.update.assert_awaited_once_with(
        id="todo-id-123",
        todo=expected_updated_todo,
    )


async def test_update_todo_suspended_user_fails() -> None:
    id_generator = mock_id_generator()
    todo_repo = mock_todo_repository()

    user_client = mock_user_client()
    user_client.get_user_status.return_value = UserStatus.SUSPENDED

    use_cases = TodoUseCases(
        id_generator=id_generator,
        todo_repo=todo_repo,
        user_client=user_client,
    )

    with pytest.raises(DomainError) as error:
        await use_cases.update(
            id="todo-id-123",
            name="New name",
            completed=True,
            user_id="user-1",
        )

    assert error.value.type == ErrorType.FORBIDDEN
    assert error.value.user_msg == "User is suspended"

    user_client.get_user_status.assert_awaited_once_with(user_id="user-1")
    todo_repo.get_by_id.assert_not_awaited()
    todo_repo.update.assert_not_awaited()


async def test_update_todo_not_found_fails() -> None:
    id_generator = mock_id_generator()

    todo_repo = mock_todo_repository()
    todo_repo.get_by_id.return_value = None

    user_client = mock_user_client()
    user_client.get_user_status.return_value = UserStatus.ACTIVE

    use_cases = TodoUseCases(
        id_generator=id_generator,
        todo_repo=todo_repo,
        user_client=user_client,
    )

    with pytest.raises(DomainError) as error:
        await use_cases.update(
            id="non-existent-id",
            name="New name",
            completed=True,
            user_id="user-1",
        )

    assert error.value.type == ErrorType.NOT_FOUND
    assert error.value.user_msg == "Todo not found"
    assert error.value.msg == "Todo with id non-existent-id for user-1 not found"

    user_client.get_user_status.assert_awaited_once_with(user_id="user-1")
    todo_repo.get_by_id.assert_awaited_once_with(id="non-existent-id")
    todo_repo.update.assert_not_awaited()


async def test_update_todo_wrong_owner_fails() -> None:
    id_generator = mock_id_generator()

    todo_repo = mock_todo_repository()
    foreign_todo = Todo(
        id="todo-id-123",
        name="Buy groceries",
        completed=False,
        user_id="user-2",
    )
    todo_repo.get_by_id.return_value = foreign_todo

    user_client = mock_user_client()
    user_client.get_user_status.return_value = UserStatus.ACTIVE

    use_cases = TodoUseCases(
        id_generator=id_generator,
        todo_repo=todo_repo,
        user_client=user_client,
    )

    with pytest.raises(DomainError) as error:
        await use_cases.update(
            id="todo-id-123",
            name="New name",
            completed=True,
            user_id="user-1",
        )

    assert error.value.type == ErrorType.NOT_FOUND
    assert error.value.user_msg == "Todo not found"

    user_client.get_user_status.assert_awaited_once_with(user_id="user-1")
    todo_repo.get_by_id.assert_awaited_once_with(id="todo-id-123")
    todo_repo.update.assert_not_awaited()
