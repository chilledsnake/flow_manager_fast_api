from app.modules.flows.models import ConditionDef, FlowDef, TaskDef


def _make_simple_flow(
    start_task: str = "t1",
    tasks: list[TaskDef] | None = None,
    conditions: list[ConditionDef] | None = None,
) -> FlowDef:
    if tasks is None:
        tasks = [
            TaskDef(name="t1", description="First"),
            TaskDef(name="t2", description="Second"),
        ]
    if conditions is None:
        conditions = [
            ConditionDef(
                name="c1",
                source_task="t1",
                target_task_success="t2",
                target_task_failure=None,
            )
        ]
    return FlowDef(
        id="test-flow",
        name="Test flow",
        start_task=start_task,
        tasks=tasks,
        conditions=conditions,
    )
