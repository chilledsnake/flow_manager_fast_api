from app.modules.flows.models import FlowDef


class FlowRepository:
    def __init__(self) -> None:
        self._flows: dict[str, FlowDef] = {}

    async def create(self, flow: FlowDef) -> FlowDef:
        self._flows[flow.id] = flow
        return flow

    async def get(self, flow_id: str) -> FlowDef | None:
        return self._flows.get(flow_id)

    async def list_all(self) -> list[FlowDef]:
        return list(self._flows.values())

    async def update(self, flow_id: str, flow: FlowDef) -> FlowDef | None:
        if flow_id not in self._flows:
            return None
        self._flows[flow_id] = flow
        return flow

    async def delete(self, flow_id: str) -> bool:
        return self._flows.pop(flow_id, None) is not None
