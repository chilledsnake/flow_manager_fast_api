from app.modules.flows.executor import FlowExecutor
from app.modules.executions.models import FlowExecution
from app.modules.executions.repository import ExecutionRepository
from app.modules.flows.repository import FlowRepository
from app.modules.tasks.repository import TaskRepository


class ExecutionService:
    def __init__(
        self,
        execution_repo: ExecutionRepository,
        flow_repo: FlowRepository,
        task_repo: TaskRepository,
    ) -> None:
        self._execution_repo = execution_repo
        self._flow_repo = flow_repo
        self._task_repo = task_repo

    async def execute(self, flow_id: str) -> FlowExecution:
        flow_def = await self._flow_repo.get(flow_id)
        if flow_def is None:
            raise ValueError("Flow not found")
        executor = FlowExecutor(flow_def, self._task_repo)
        return await self._execution_repo.save(await executor.run())

    async def get(self, execution_id: str) -> FlowExecution | None:
        return await self._execution_repo.get(execution_id)

    async def list_all(self, flow_id: str | None = None) -> list[FlowExecution]:
        if flow_id is not None:
            return await self._execution_repo.list_by_flow(flow_id)
        return await self._execution_repo.list_all()
