import pytest

from app.modules.flows.models import FlowCreateRequest, FlowDef, TaskDef
from app.modules.flows.repository import FlowRepository
from app.modules.flows.service import FlowService

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
def service():
    repo = FlowRepository()
    return FlowService(repo)


async def test_create(service):
    flow = _make_flow()
    result = await service.create(FlowCreateRequest(flow=flow))
    assert result.id == "f1"


async def test_create_duplicate_raises(service):
    flow = _make_flow()
    await service.create(FlowCreateRequest(flow=flow))
    with pytest.raises(ValueError, match="already exists"):
        await service.create(FlowCreateRequest(flow=flow))


async def test_get(service):
    flow = _make_flow()
    await service.create(FlowCreateRequest(flow=flow))
    result = await service.get("f1")
    assert result is not None
    assert result.id == "f1"


async def test_get_missing_returns_none(service):
    assert await service.get("missing") is None


async def test_list_all(service):
    await service.create(FlowCreateRequest(flow=_make_flow("f1")))
    await service.create(FlowCreateRequest(flow=_make_flow("f2")))
    flows = await service.list_all()
    assert len(flows) == 2


async def test_update(service):
    flow = _make_flow()
    await service.create(FlowCreateRequest(flow=flow))
    updated = _make_flow()
    updated.name = "Updated"
    result = await service.update("f1", FlowCreateRequest(flow=updated))
    assert result.name == "Updated"


async def test_update_missing_raises(service):
    with pytest.raises(ValueError, match="not found"):
        await service.update("missing", FlowCreateRequest(flow=_make_flow()))


async def test_delete(service):
    await service.create(FlowCreateRequest(flow=_make_flow()))
    assert await service.delete("f1") is True
    assert await service.get("f1") is None


async def test_delete_missing_returns_false(service):
    assert await service.delete("missing") is False
