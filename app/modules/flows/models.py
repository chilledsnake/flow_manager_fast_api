from pydantic import BaseModel, Field, field_validator, model_validator


class TaskDef(BaseModel):
    name: str = Field(pattern=r"^[a-zA-Z0-9_]+$")
    description: str = ""


class ConditionDef(BaseModel):
    name: str
    description: str = ""
    source_task: str
    outcome: str = "success"
    target_task_success: str | None = None
    target_task_failure: str | None = None

    @field_validator("target_task_success", "target_task_failure", mode="before")
    @classmethod
    def normalize_end(cls, v: str | None) -> str | None:
        if v == "end":
            return None
        return v


class FlowDef(BaseModel):
    id: str
    name: str
    start_task: str
    tasks: list[TaskDef]
    conditions: list[ConditionDef]

    @model_validator(mode="after")
    def validate_references(self) -> "FlowDef":
        task_names = {t.name for t in self.tasks}
        if self.start_task not in task_names:
            msg = f"start_task '{self.start_task}' not found in tasks"
            raise ValueError(msg)
        for cond in self.conditions:
            if cond.source_task not in task_names:
                msg = f"condition '{cond.name}' references unknown source_task '{cond.source_task}'"
                raise ValueError(msg)
            for target in (cond.target_task_success, cond.target_task_failure):
                if target is not None and target not in task_names:
                    msg = f"condition '{cond.name}' references unknown target_task '{target}'"
                    raise ValueError(msg)
        return self


class FlowCreateRequest(BaseModel):
    flow: FlowDef
