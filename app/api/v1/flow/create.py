from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_flow_service
from app.modules.flows.models import FlowCreateRequest, FlowDef
from app.modules.flows.service import FlowService

router = APIRouter()


@router.post("/", response_model=FlowDef, status_code=201)
async def create_flow(
    req: FlowCreateRequest, service: FlowService = Depends(get_flow_service)
):
    try:
        return await service.create(req)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
