from functools import lru_cache

from app.modules.executions.repository import ExecutionRepository
from app.modules.executions.service import ExecutionService
from app.modules.flows.repository import FlowRepository
from app.modules.flows.service import FlowService
from app.modules.tasks.repository import TaskRepository


@lru_cache
def get_task_repository() -> TaskRepository:
    return TaskRepository()


@lru_cache
def get_flow_repository() -> FlowRepository:
    return FlowRepository()


@lru_cache
def get_execution_repository() -> ExecutionRepository:
    return ExecutionRepository()


def get_flow_service() -> FlowService:
    return FlowService(get_flow_repository())


def get_execution_service() -> ExecutionService:
    return ExecutionService(
        get_execution_repository(), get_flow_repository(), get_task_repository()
    )
