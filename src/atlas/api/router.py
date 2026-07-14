from fastapi import APIRouter

from atlas.api.accounts import router as account_router
from atlas.api.routes import router as health_router

router = APIRouter(prefix="/api/v1")

router.include_router(health_router)
router.include_router(account_router)
