from fastapi import APIRouter
from app.api.v1.flow import router as flow_router
from app.api.v1.execution import router as execution_router

router = APIRouter(prefix="/v1")

router.include_router(flow_router)
router.include_router(execution_router)
