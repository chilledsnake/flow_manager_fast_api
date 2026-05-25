from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_execution_service
from app.modules.executions.models import FlowExecution
from app.modules.executions.service import ExecutionService

router = APIRouter()


@router.get("/{execution_id}/", response_model=FlowExecution)
async def get_execution(
    execution_id: str, service: ExecutionService = Depends(get_execution_service)
):
    execution = await service.get(execution_id)
    if execution is None:
        raise HTTPException(status_code=404, detail="Execution not found")
    return execution
