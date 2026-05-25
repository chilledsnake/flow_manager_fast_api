from fastapi import APIRouter, Depends

from app.dependencies import get_execution_service
from app.modules.executions.models import FlowExecution
from app.modules.executions.service import ExecutionService

router = APIRouter()


@router.get("/", response_model=list[FlowExecution])
async def list_executions(
    flow_id: str | None = None,
    service: ExecutionService = Depends(get_execution_service),
):
    return await service.list_all(flow_id=flow_id)
