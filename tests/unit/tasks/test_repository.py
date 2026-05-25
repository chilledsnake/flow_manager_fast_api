import pytest

from app.modules.tasks.repository import TaskRepository
from app.modules.tasks.utils import register_handlers

pytestmark = pytest.mark.asyncio


async def test_register_and_get():
    reg = TaskRepository()

    async def sample_handler(ctx: dict) -> dict:
        return {"result": 42}

    await reg.register("test_task", sample_handler)
    assert await reg.get("test_task") is sample_handler


async def test_get_unregistered_returns_none():
    reg = TaskRepository()
    assert await reg.get("nonexistent") is None


async def test_decorator_registers_via_pending():
    from app.modules.tasks.utils import task_handler, _pending

    # Clear pending to avoid interference from handlers module
    original_pending = _pending[:]
    _pending.clear()

    try:

        @task_handler("test_pending_task")
        async def my_handler(ctx: dict) -> dict:
            return {"ok": True}

        reg = TaskRepository()
        register_handlers(reg)
        assert await reg.get("test_pending_task") is my_handler
    finally:
        _pending.clear()
        _pending.extend(original_pending)


async def test_list_handlers():
    reg = TaskRepository()

    async def handler_a(ctx: dict) -> dict:
        return {}

    async def handler_b(ctx: dict) -> dict:
        return {}

    await reg.register("a", handler_a)
    await reg.register("b", handler_b)
    listing = await reg.list_handlers()
    assert "a" in listing
    assert "b" in listing
