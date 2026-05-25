from fastapi import APIRouter
from app.api.v1.execution.list import router as list_router
from app.api.v1.execution.retrieve import router as retrieve_router

router = APIRouter(prefix="/execution", tags=["Execution"])
router.include_router(list_router)
router.include_router(retrieve_router)
