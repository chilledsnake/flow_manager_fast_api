from app.modules.executions.models import FlowExecution


class ExecutionRepository:
    def __init__(self) -> None:
        self._executions: dict[str, FlowExecution] = {}

    async def save(self, execution: FlowExecution) -> FlowExecution:
        self._executions[execution.id] = execution
        return execution

    async def get(self, execution_id: str) -> FlowExecution | None:
        return self._executions.get(execution_id)

    async def list_by_flow(self, flow_id: str) -> list[FlowExecution]:
        return [e for e in self._executions.values() if e.flow_id == flow_id]

    async def list_all(self) -> list[FlowExecution]:
        return list(self._executions.values())
