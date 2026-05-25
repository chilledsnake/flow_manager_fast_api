import pytest

from app.modules.executions.repository import ExecutionRepository
from app.modules.executions.service import ExecutionService
from app.modules.flows.models import FlowCreateRequest, FlowDef, TaskDef
from app.modules.flows.repository import FlowRepository
from app.modules.flows.service import FlowService
from app.modules.tasks.repository import TaskRepository
from app.modules.tasks.utils import register_handlers

pytestmark = pytest.mark.asyncio


def _make_flow(flow_id: str = "f1") -> FlowDef:
    return FlowDef(
        id=flow_id,
        name="Test flow",
        start_task="t1",
        tasks=[TaskDef(name="t1", description="First")],
        conditions=[],
    )


@pytest.fixture
def repos():
    flow_repo = FlowRepository()
    execution_repo = ExecutionRepository()
    task_repo = TaskRepository()
    register_handlers(task_repo)
    return flow_repo, execution_repo, task_repo


@pytest.fixture
def service(repos):
    return ExecutionService(repos[1], repos[0], repos[2])


@pytest.fixture
def flow_service(repos):
    return FlowService(repos[0])


async def test_execute(service, flow_service):
    flow = _make_flow()
    await flow_service.create(FlowCreateRequest(flow=flow))
    result = await service.execute("f1")
    assert result.flow_id == "f1"


async def test_execute_missing_flow_raises(service):
    with pytest.raises(ValueError, match="not found"):
        await service.execute("missing")


async def test_get(service, flow_service):
    flow = _make_flow()
    await flow_service.create(FlowCreateRequest(flow=flow))
    execution = await service.execute("f1")
    result = await service.get(execution.id)
    assert result is not None
    assert result.id == execution.id


async def test_get_missing_returns_none(service):
    assert await service.get("missing") is None


async def test_list_all(service, flow_service):
    flow = _make_flow("f1")
    await flow_service.create(FlowCreateRequest(flow=flow))
    await service.execute("f1")
    executions = await service.list_all()
    assert len(executions) == 1


async def test_list_by_flow(service, flow_service):
    await flow_service.create(FlowCreateRequest(flow=_make_flow("f1")))
    await flow_service.create(FlowCreateRequest(flow=_make_flow("f2")))
    await service.execute("f1")
    await service.execute("f1")
    await service.execute("f2")

    f1_executions = await service.list_all(flow_id="f1")
    assert len(f1_executions) == 2
    assert all(e.flow_id == "f1" for e in f1_executions)


async def test_list_by_flow_no_match(service, flow_service):
    await flow_service.create(FlowCreateRequest(flow=_make_flow("f1")))
    await service.execute("f1")
    assert await service.list_all(flow_id="nonexistent") == []
