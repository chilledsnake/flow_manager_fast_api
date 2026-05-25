from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_execution_service
from app.modules.executions.models import FlowExecution
from app.modules.executions.service import ExecutionService

router = APIRouter()


@router.post("/{flow_id}/execute", response_model=FlowExecution, status_code=202)
async def execute_flow(
    flow_id: str, service: ExecutionService = Depends(get_execution_service)
):
    try:
        return await service.execute(flow_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Flow not found")
