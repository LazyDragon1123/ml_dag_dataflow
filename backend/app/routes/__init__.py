from fastapi import APIRouter

from app.routes.analytics import router as analytics_router

router = APIRouter()
router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
