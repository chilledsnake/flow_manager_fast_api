from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_flow_service
from app.modules.flows.service import FlowService

router = APIRouter()


@router.delete("/{flow_id}", status_code=204)
async def delete_flow(flow_id: str, service: FlowService = Depends(get_flow_service)):
    if not await service.delete(flow_id):
        raise HTTPException(status_code=404, detail="Flow not found")
