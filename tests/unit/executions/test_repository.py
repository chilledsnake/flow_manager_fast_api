import pytest

from app.modules.executions.models import FlowExecution
from app.modules.executions.repository import ExecutionRepository
from app.modules.flows.models import FlowDef, TaskDef


def _make_execution(exec_id: str = "exec1", flow_id: str = "f1") -> FlowExecution:
    flow = FlowDef(
        id=flow_id,
        name="Test",
        start_task="t1",
        tasks=[TaskDef(name="t1", description="First")],
        conditions=[],
    )
    return FlowExecution(id=exec_id, flow_id=flow_id, flow_def=flow)


pytestmark = pytest.mark.asyncio


async def test_save_and_get():
    repo = ExecutionRepository()
    execution = _make_execution()
    saved = await repo.save(execution)
    assert saved.id == "exec1"
    result = await repo.get("exec1")
    assert result is not None
    assert result.id == "exec1"


async def test_get_missing_returns_none():
    repo = ExecutionRepository()
    assert await repo.get("missing") is None


async def test_list_all():
    repo = ExecutionRepository()
    await repo.save(_make_execution("e1", "f1"))
    await repo.save(_make_execution("e2", "f2"))
    executions = await repo.list_all()
    assert len(executions) == 2


async def test_list_all_empty():
    repo = ExecutionRepository()
    assert await repo.list_all() == []


async def test_list_by_flow():
    repo = ExecutionRepository()
    await repo.save(_make_execution("e1", "f1"))
    await repo.save(_make_execution("e2", "f2"))
    await repo.save(_make_execution("e3", "f1"))
    f1_executions = await repo.list_by_flow("f1")
    assert len(f1_executions) == 2
    assert all(e.flow_id == "f1" for e in f1_executions)


async def test_list_by_flow_no_match():
    repo = ExecutionRepository()
    await repo.save(_make_execution("e1", "f1"))
    assert await repo.list_by_flow("missing") == []
