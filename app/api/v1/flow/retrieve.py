from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_flow_service
from app.modules.flows.models import FlowDef
from app.modules.flows.service import FlowService

router = APIRouter()


@router.get("/{flow_id}", response_model=FlowDef)
async def get_flow(flow_id: str, service: FlowService = Depends(get_flow_service)):
    flow = await service.get(flow_id)
    if flow is None:
        raise HTTPException(status_code=404, detail="Flow not found")
    return flow
