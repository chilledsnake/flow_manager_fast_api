from __future__ import annotations

from app.modules.tasks.models import TaskHandler
from app.modules.tasks.repository import TaskRepository

_pending: list[tuple[str, TaskHandler]] = []


def task_handler(name: str):
    def decorator(fn: TaskHandler) -> TaskHandler:
        _pending.append((name, fn))
        return fn

    return decorator


def register_handlers(registry: TaskRepository) -> None:
    for name, handler in _pending:
        registry._handlers[name] = handler
