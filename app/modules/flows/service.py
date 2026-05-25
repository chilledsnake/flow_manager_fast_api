from app.modules.flows.models import FlowCreateRequest, FlowDef
from app.modules.flows.repository import FlowRepository


class FlowService:
    def __init__(self, repository: FlowRepository) -> None:
        self._repository = repository

    async def create(self, req: FlowCreateRequest) -> FlowDef:
        flow = req.flow
        if await self._repository.get(flow.id) is not None:
            raise ValueError(f"Flow '{flow.id}' already exists")
        return await self._repository.create(flow)

    async def get(self, flow_id: str) -> FlowDef | None:
        return await self._repository.get(flow_id)

    async def list_all(self) -> list[FlowDef]:
        return await self._repository.list_all()

    async def update(self, flow_id: str, req: FlowCreateRequest) -> FlowDef:
        existing = await self._repository.get(flow_id)
        if existing is None:
            raise ValueError("Flow not found")
        return await self._repository.update(flow_id, req.flow)

    async def delete(self, flow_id: str) -> bool:
        return await self._repository.delete(flow_id)
