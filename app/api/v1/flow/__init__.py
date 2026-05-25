from fastapi import APIRouter
from app.api.v1.flow.create import router as create_router
from app.api.v1.flow.delete import router as delete_router
from app.api.v1.flow.list import router as list_router
from app.api.v1.flow.retrieve import router as retrieve_router
from app.api.v1.flow.update import router as update_router
from app.api.v1.flow.execute import router as execute_router


router = APIRouter(prefix="/flow", tags=["Flow"])

router.include_router(create_router)
router.include_router(delete_router)
router.include_router(list_router)
router.include_router(retrieve_router)
router.include_router(update_router)
router.include_router(execute_router)
