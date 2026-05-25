import pytest
from unittest.mock import AsyncMock

from app.modules.executions.service import ExecutionService
from app.modules.flows.models import FlowDef, TaskDef


def _make_flow(flow_id: str = "f1") -> FlowDef:
    return FlowDef(
        id=flow_id,
        name="Test flow",
        start_task="t1",
        tasks=[TaskDef(name="t1", description="First")],
        conditions=[],
    )


pytestmark = pytest.mark.asyncio


async def test_execute_calls_repos():
    flow = _make_flow()
    flow_repo = AsyncMock()
    flow_repo.get.return_value = flow
    execution_repo = AsyncMock()
    task_repo = AsyncMock()
    service = ExecutionService(execution_repo, flow_repo, task_repo)
    await service.execute("f1")
    flow_repo.get.assert_awaited_once_with("f1")
    execution_repo.save.assert_awaited_once()


async def test_execute_raises_on_missing_flow():
    flow_repo = AsyncMock()
    flow_repo.get.return_value = None
    execution_repo = AsyncMock()
    task_repo = AsyncMock()
    service = ExecutionService(execution_repo, flow_repo, task_repo)
    with pytest.raises(ValueError, match="not found"):
        await service.execute("missing")
    execution_repo.save.assert_not_awaited()


async def test_get_delegates_to_repository():
    execution_repo = AsyncMock()
    flow_repo = AsyncMock()
    task_repo = AsyncMock()
    service = ExecutionService(execution_repo, flow_repo, task_repo)
    await service.get("exec1")
    execution_repo.get.assert_awaited_once_with("exec1")


async def test_list_all_delegates_to_repository():
    execution_repo = AsyncMock()
    flow_repo = AsyncMock()
    task_repo = AsyncMock()
    service = ExecutionService(execution_repo, flow_repo, task_repo)
    await service.list_all()
    execution_repo.list_all.assert_awaited_once()


async def test_list_all_with_flow_id():
    execution_repo = AsyncMock()
    flow_repo = AsyncMock()
    task_repo = AsyncMock()
    service = ExecutionService(execution_repo, flow_repo, task_repo)
    await service.list_all(flow_id="f1")
    execution_repo.list_by_flow.assert_awaited_once_with("f1")
    execution_repo.list_all.assert_not_awaited()
