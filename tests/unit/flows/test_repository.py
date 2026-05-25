import pytest

from app.modules.flows.models import FlowDef, TaskDef
from app.modules.flows.repository import FlowRepository


def _make_flow(flow_id: str = "f1") -> FlowDef:
    return FlowDef(
        id=flow_id,
        name="Test flow",
        start_task="t1",
        tasks=[TaskDef(name="t1", description="First")],
        conditions=[],
    )


pytestmark = pytest.mark.asyncio


async def test_create_and_get():
    repo = FlowRepository()
    flow = _make_flow()
    created = await repo.create(flow)
    assert created.id == "f1"
    result = await repo.get("f1")
    assert result is not None
    assert result.id == "f1"


async def test_get_missing_returns_none():
    repo = FlowRepository()
    assert await repo.get("missing") is None


async def test_list_all():
    repo = FlowRepository()
    await repo.create(_make_flow("f1"))
    await repo.create(_make_flow("f2"))
    flows = await repo.list_all()
    assert len(flows) == 2
    assert {f.id for f in flows} == {"f1", "f2"}


async def test_list_all_empty():
    repo = FlowRepository()
    assert await repo.list_all() == []


async def test_update():
    repo = FlowRepository()
    await repo.create(_make_flow("f1"))
    updated = _make_flow("f1")
    updated.name = "Updated"
    result = await repo.update("f1", updated)
    assert result.name == "Updated"


async def test_update_missing_returns_none():
    repo = FlowRepository()
    result = await repo.update("missing", _make_flow("missing"))
    assert result is None


async def test_delete():
    repo = FlowRepository()
    await repo.create(_make_flow("f1"))
    assert await repo.delete("f1") is True
    assert await repo.get("f1") is None


async def test_delete_missing_returns_false():
    repo = FlowRepository()
    assert await repo.delete("missing") is False
