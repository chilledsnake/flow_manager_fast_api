import uuid
from datetime import UTC, datetime

from app.modules.tasks.repository import TaskRepository
from app.modules.executions.models import (
    FlowExecution,
    FlowExecutionStatus,
    TaskResult,
    TaskStatus,
)
from app.modules.flows.models import FlowDef


class FlowExecutor:
    def __init__(self, flow_def: FlowDef, task_registry: TaskRepository) -> None:
        self.flow_def = flow_def
        self.task_registry = task_registry
        self.execution = FlowExecution(
            id=str(uuid.uuid4()),
            flow_id=flow_def.id,
            flow_def=flow_def.model_copy(deep=True),
        )

    async def run(self) -> FlowExecution:
        self.execution.status = FlowExecutionStatus.RUNNING
        context: dict[str, dict] = {}

        for task_name in self._walk():
            self.execution.current_task = task_name
            result = await self._execute_task(task_name, context)
            self.execution.results[task_name] = result
            context[task_name] = result.output or {}

        failed = any(
            r.status == TaskStatus.FAILURE for r in self.execution.results.values()
        )
        self.execution.status = (
            FlowExecutionStatus.FAILED if failed else FlowExecutionStatus.COMPLETED
        )
        self.execution.finished_at = datetime.now(UTC)
        self.execution.current_task = None
        return self.execution

    def _walk(self):
        task_name: str | None = self.flow_def.start_task
        while task_name is not None:
            yield task_name
            result = self.execution.results[task_name]
            task_name = self._resolve_next_task(task_name, result.status)

    def _resolve_next_task(self, task_name: str, status: TaskStatus) -> str | None:
        for cond in self.flow_def.conditions:
            if cond.source_task != task_name:
                continue
            if status == TaskStatus.SUCCESS:
                return cond.target_task_success
            return cond.target_task_failure
        return None

    async def _execute_task(
        self, task_name: str, context: dict[str, dict]
    ) -> TaskResult:
        handler = await self.task_registry.get(task_name)
        if handler is None:
            return TaskResult(
                task_name=task_name,
                status=TaskStatus.FAILURE,
                error=f"No handler registered for task '{task_name}'",
            )

        started = datetime.now(UTC)
        try:
            output = await handler(context)
            return TaskResult(
                task_name=task_name,
                status=TaskStatus.SUCCESS,
                started_at=started,
                finished_at=datetime.now(UTC),
                output=output,
            )
        except Exception as exc:
            return TaskResult(
                task_name=task_name,
                status=TaskStatus.FAILURE,
                started_at=started,
                finished_at=datetime.now(UTC),
                error=str(exc),
            )
