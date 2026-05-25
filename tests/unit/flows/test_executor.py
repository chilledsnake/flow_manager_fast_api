import pytest

from app.modules.flows.executor import FlowExecutor
from app.modules.tasks.repository import TaskRepository
from app.modules.executions.models import FlowExecutionStatus, TaskStatus
from app.modules.flows.models import ConditionDef, TaskDef

from .conftest import _make_simple_flow

pytestmark = pytest.mark.asyncio


async def test_successful_two_task_flow():
    reg = TaskRepository()

    async def h1(ctx: dict) -> dict:
        return {"step": 1}

    async def h2(ctx: dict) -> dict:
        return {"step": 2}

    await reg.register("t1", h1)
    await reg.register("t2", h2)

    flow = _make_simple_flow()
    result = await FlowExecutor(flow, reg).run()
    assert result.status == FlowExecutionStatus.COMPLETED
    assert len(result.results) == 2
    assert result.results["t1"].status == TaskStatus.SUCCESS
    assert result.results["t2"].status == TaskStatus.SUCCESS


async def test_failure_ends_flow():
    reg = TaskRepository()

    async def failing_handler(ctx: dict) -> dict:
        raise RuntimeError("boom")

    async def h2(ctx: dict) -> dict:
        return {"step": 2}

    await reg.register("t1", failing_handler)
    await reg.register("t2", h2)

    flow = _make_simple_flow()
    result = await FlowExecutor(flow, reg).run()
    assert result.status == FlowExecutionStatus.FAILED
    assert result.results["t1"].status == TaskStatus.FAILURE
    assert "t2" not in result.results


async def test_missing_handler_fails():
    reg = TaskRepository()

    flow = _make_simple_flow()
    result = await FlowExecutor(flow, reg).run()
    assert result.status == FlowExecutionStatus.FAILED
    assert "No handler registered" in result.results["t1"].error


async def test_context_accumulation():
    reg = TaskRepository()

    async def h1(ctx: dict) -> dict:
        return {"value": 10}

    async def h2(ctx: dict) -> dict:
        return {"doubled": ctx["t1"]["value"] * 2}

    await reg.register("t1", h1)
    await reg.register("t2", h2)

    flow = _make_simple_flow()
    result = await FlowExecutor(flow, reg).run()
    assert result.results["t2"].output == {"doubled": 20}


async def test_no_condition_ends_flow():
    reg = TaskRepository()

    async def h1(ctx: dict) -> dict:
        return {"done": True}

    await reg.register("t1", h1)

    flow = _make_simple_flow(conditions=[])
    result = await FlowExecutor(flow, reg).run()
    assert result.status == FlowExecutionStatus.COMPLETED
    assert len(result.results) == 1


async def test_failure_routes_to_failure_target():
    tasks = [
        TaskDef(name="t1", description="First"),
        TaskDef(name="t2", description="Second"),
        TaskDef(name="rollback", description="Rollback"),
    ]
    conditions = [
        ConditionDef(
            name="c1",
            source_task="t1",
            target_task_success="t2",
            target_task_failure="rollback",
        ),
    ]

    async def fail_handler(ctx: dict) -> dict:
        raise RuntimeError("fail")

    async def h2(ctx: dict) -> dict:
        return {"step": 2}

    async def rollback_handler(ctx: dict) -> dict:
        return {"rolled_back": True}

    reg = TaskRepository()
    await reg.register("t1", fail_handler)
    await reg.register("t2", h2)
    await reg.register("rollback", rollback_handler)

    flow = _make_simple_flow(tasks=tasks, conditions=conditions)
    result = await FlowExecutor(flow, reg).run()
    assert result.status == FlowExecutionStatus.FAILED
    assert "rollback" in result.results
    assert result.results["rollback"].status == TaskStatus.SUCCESS
