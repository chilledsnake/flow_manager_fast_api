from app.modules.executions.models import (
    FlowExecution,
    FlowExecutionStatus,
    TaskResult,
    TaskStatus,
)
from app.modules.flows.models import FlowDef, TaskDef


def test_task_status_values():
    assert TaskStatus.PENDING == "pending"
    assert TaskStatus.RUNNING == "running"
    assert TaskStatus.SUCCESS == "success"
    assert TaskStatus.FAILURE == "failure"
    assert TaskStatus.SKIPPED == "skipped"


def test_flow_execution_status_values():
    assert FlowExecutionStatus.PENDING == "pending"
    assert FlowExecutionStatus.RUNNING == "running"
    assert FlowExecutionStatus.COMPLETED == "completed"
    assert FlowExecutionStatus.FAILED == "failed"


def test_task_result_success():
    result = TaskResult(
        task_name="t1",
        status=TaskStatus.SUCCESS,
        output={"key": "value"},
    )
    assert result.task_name == "t1"
    assert result.status == TaskStatus.SUCCESS
    assert result.output == {"key": "value"}
    assert result.error is None


def test_task_result_failure():
    result = TaskResult(
        task_name="t1",
        status=TaskStatus.FAILURE,
        error="something went wrong",
    )
    assert result.status == TaskStatus.FAILURE
    assert result.error == "something went wrong"
    assert result.output is None


def test_flow_execution_defaults():
    flow = FlowDef(
        id="f1",
        name="Test",
        start_task="t1",
        tasks=[TaskDef(name="t1", description="First")],
        conditions=[],
    )
    execution = FlowExecution(id="exec1", flow_id="f1", flow_def=flow)
    assert execution.status == FlowExecutionStatus.PENDING
    assert execution.results == {}
    assert execution.current_task is None
    assert execution.finished_at is None
