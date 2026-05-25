from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_flow_service
from app.modules.flows.models import FlowCreateRequest, FlowDef
from app.modules.flows.service import FlowService

router = APIRouter()


@router.put("/{flow_id}", response_model=FlowDef)
async def update_flow(
    flow_id: str,
    req: FlowCreateRequest,
    service: FlowService = Depends(get_flow_service),
):
    try:
        return await service.update(flow_id, req)
    except ValueError:
        raise HTTPException(status_code=404, detail="Flow not found")
