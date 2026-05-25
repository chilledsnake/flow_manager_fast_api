import copy

import pytest
from fastapi.testclient import TestClient

from app.dependencies import (
    get_execution_repository,
    get_execution_service,
    get_flow_repository,
    get_flow_service,
    get_task_repository,
)
from app.modules.executions.repository import ExecutionRepository
from app.modules.executions.service import ExecutionService
from app.modules.flows.repository import FlowRepository
from app.modules.flows.service import FlowService
from app.modules.tasks.repository import TaskRepository
from app.modules.tasks.utils import register_handlers
from app.main import app


@pytest.fixture(autouse=True)
def reset_di():
    fresh_flow_repo = FlowRepository()
    fresh_execution_repo = ExecutionRepository()
    fresh_task_repo = TaskRepository()
    register_handlers(fresh_task_repo)

    app.dependency_overrides[get_flow_repository] = lambda: fresh_flow_repo
    app.dependency_overrides[get_execution_repository] = lambda: fresh_execution_repo
    app.dependency_overrides[get_task_repository] = lambda: fresh_task_repo
    app.dependency_overrides[get_flow_service] = lambda: FlowService(fresh_flow_repo)
    app.dependency_overrides[get_execution_service] = lambda: ExecutionService(
        fresh_execution_repo, fresh_flow_repo, fresh_task_repo
    )

    yield

    app.dependency_overrides.clear()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_flow():
    return {"flow": copy.deepcopy(_SAMPLE_FLOW)}


_SAMPLE_FLOW = {
    "id": "flow123",
    "name": "Data processing flow",
    "start_task": "task1",
    "tasks": [
        {"name": "task1", "description": "Fetch data"},
        {"name": "task2", "description": "Process data"},
        {"name": "task3", "description": "Store data"},
    ],
    "conditions": [
        {
            "name": "condition_task1_result",
            "description": "Evaluate the result of task1",
            "source_task": "task1",
            "outcome": "success",
            "target_task_success": "task2",
            "target_task_failure": None,
        },
        {
            "name": "condition_task2_result",
            "description": "Evaluate the result of task2",
            "source_task": "task2",
            "outcome": "success",
            "target_task_success": "task3",
            "target_task_failure": None,
        },
    ],
}
