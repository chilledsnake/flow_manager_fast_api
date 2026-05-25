import pytest

from app.modules.flows.models import ConditionDef, FlowCreateRequest, FlowDef, TaskDef


def test_valid_flow():
    flow = FlowDef(
        id="f1",
        name="Test",
        start_task="t1",
        tasks=[TaskDef(name="t1", description="First")],
        conditions=[],
    )
    assert flow.id == "f1"


def test_start_task_not_in_tasks():
    with pytest.raises(ValueError, match="start_task"):
        FlowDef(
            id="f1",
            name="Test",
            start_task="missing",
            tasks=[TaskDef(name="t1", description="First")],
            conditions=[],
        )


def test_condition_source_task_not_in_tasks():
    with pytest.raises(ValueError, match="source_task"):
        FlowDef(
            id="f1",
            name="Test",
            start_task="t1",
            tasks=[TaskDef(name="t1", description="First")],
            conditions=[
                ConditionDef(
                    name="c1",
                    source_task="missing",
                    target_task_success=None,
                )
            ],
        )


def test_condition_target_task_not_in_tasks():
    with pytest.raises(ValueError, match="target_task"):
        FlowDef(
            id="f1",
            name="Test",
            start_task="t1",
            tasks=[TaskDef(name="t1", description="First")],
            conditions=[
                ConditionDef(
                    name="c1",
                    source_task="t1",
                    target_task_success="missing",
                )
            ],
        )


def test_condition_target_failure_not_in_tasks():
    with pytest.raises(ValueError, match="target_task"):
        FlowDef(
            id="f1",
            name="Test",
            start_task="t1",
            tasks=[TaskDef(name="t1", description="First")],
            conditions=[
                ConditionDef(
                    name="c1",
                    source_task="t1",
                    target_task_failure="missing",
                )
            ],
        )


def test_none_targets_are_valid():
    flow = FlowDef(
        id="f1",
        name="Test",
        start_task="t1",
        tasks=[TaskDef(name="t1", description="First")],
        conditions=[
            ConditionDef(
                name="c1",
                source_task="t1",
                target_task_success=None,
                target_task_failure=None,
            )
        ],
    )
    assert flow.conditions[0].target_task_success is None


def test_task_name_pattern_validation():
    with pytest.raises(ValueError):
        TaskDef(name="invalid name!", description="Bad")


def test_flow_create_request_wrapper():
    flow = FlowDef(
        id="f1",
        name="Test",
        start_task="t1",
        tasks=[TaskDef(name="t1", description="First")],
        conditions=[],
    )
    req = FlowCreateRequest(flow=flow)
    assert req.flow.id == "f1"


def test_end_string_normalized_to_none():
    cond = ConditionDef(
        name="c1",
        source_task="t1",
        target_task_success="t2",
        target_task_failure="end",
    )
    assert cond.target_task_failure is None


def test_end_string_in_success_target():
    cond = ConditionDef(
        name="c1",
        source_task="t1",
        target_task_success="end",
    )
    assert cond.target_task_success is None
