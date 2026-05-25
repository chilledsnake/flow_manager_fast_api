from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from app.modules.flows.models import FlowDef


class TaskStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"


class FlowExecutionStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskResult(BaseModel):
    task_name: str
    status: TaskStatus
    started_at: datetime | None = None
    finished_at: datetime | None = None
    output: dict | None = None
    error: str | None = None


class FlowExecution(BaseModel):
    id: str
    flow_id: str
    flow_def: FlowDef
    status: FlowExecutionStatus = FlowExecutionStatus.PENDING
    current_task: str | None = None
    results: dict[str, TaskResult] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    finished_at: datetime | None = None
