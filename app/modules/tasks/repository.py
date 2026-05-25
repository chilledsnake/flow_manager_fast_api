from app.modules.tasks.models import TaskHandler


class TaskRepository:
    def __init__(self) -> None:
        self._handlers: dict[str, TaskHandler] = {}

    async def register(self, task_name: str, handler: TaskHandler) -> None:
        self._handlers[task_name] = handler

    async def get(self, task_name: str) -> TaskHandler | None:
        return self._handlers.get(task_name)

    async def list_handlers(self) -> dict[str, str]:
        return {k: v.__qualname__ for k, v in self._handlers.items()}
