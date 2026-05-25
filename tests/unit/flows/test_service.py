import pytest
from unittest.mock import AsyncMock

from app.modules.flows.models import FlowCreateRequest, FlowDef, TaskDef
from app.modules.flows.service import FlowService


def _make_flow(flow_id: str = "f1") -> FlowDef:
    return FlowDef(
        id=flow_id,
        name="Test flow",
        start_task="t1",
        tasks=[TaskDef(name="t1", description="First")],
        conditions=[],
    )


pytestmark = pytest.mark.asyncio


async def test_create_calls_repository():
    repo = AsyncMock()
    repo.get.return_value = None
    flow = _make_flow()
    service = FlowService(repo)
    await service.create(FlowCreateRequest(flow=flow))
    repo.get.assert_awaited_once_with("f1")
    repo.create.assert_awaited_once_with(flow)


async def test_create_raises_on_duplicate():
    repo = AsyncMock()
    repo.get.return_value = _make_flow()
    service = FlowService(repo)
    with pytest.raises(ValueError, match="already exists"):
        await service.create(FlowCreateRequest(flow=_make_flow()))
    repo.create.assert_not_awaited()


async def test_get_delegates_to_repository():
    repo = AsyncMock()
    repo.get.return_value = _make_flow()
    service = FlowService(repo)
    result = await service.get("f1")
    repo.get.assert_awaited_once_with("f1")
    assert result.id == "f1"


async def test_get_missing_returns_none():
    repo = AsyncMock()
    repo.get.return_value = None
    service = FlowService(repo)
    result = await service.get("missing")
    assert result is None


async def test_list_all_delegates_to_repository():
    repo = AsyncMock()
    repo.list_all.return_value = []
    service = FlowService(repo)
    await service.list_all()
    repo.list_all.assert_awaited_once()


async def test_update_calls_repository():
    repo = AsyncMock()
    existing = _make_flow()
    repo.get.return_value = existing
    updated = _make_flow()
    updated.name = "Updated"
    repo.update.return_value = updated
    service = FlowService(repo)
    result = await service.update("f1", FlowCreateRequest(flow=updated))
    repo.get.assert_awaited_once_with("f1")
    repo.update.assert_awaited_once_with("f1", updated)
    assert result.name == "Updated"


async def test_update_raises_on_missing():
    repo = AsyncMock()
    repo.get.return_value = None
    service = FlowService(repo)
    with pytest.raises(ValueError, match="not found"):
        await service.update("missing", FlowCreateRequest(flow=_make_flow()))
    repo.update.assert_not_awaited()


async def test_delete_delegates_to_repository():
    repo = AsyncMock()
    repo.delete.return_value = True
    service = FlowService(repo)
    result = await service.delete("f1")
    repo.delete.assert_awaited_once_with("f1")
    assert result is True
