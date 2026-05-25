from fastapi import APIRouter, Depends

from app.dependencies import get_flow_service
from app.modules.flows.models import FlowDef
from app.modules.flows.service import FlowService

router = APIRouter()


@router.get("/", response_model=list[FlowDef])
async def list_flows(service: FlowService = Depends(get_flow_service)):
    return await service.list_all()
