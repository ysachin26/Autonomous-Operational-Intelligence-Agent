"""
AOIA ML Engine - API Routes
"""

from fastapi import APIRouter
from app.api.detect import router as detect_router
from app.api.analyze import router as analyze_router
from app.api.chat import router as chat_router
from app.api.optimize import router as optimize_router

router = APIRouter()

router.include_router(detect_router, prefix="/detect", tags=["Anomaly Detection"])
router.include_router(analyze_router, prefix="/analyze", tags=["Analysis"])
router.include_router(chat_router, tags=["Chat & Reasoning"])
router.include_router(optimize_router, prefix="/optimize", tags=["Optimization"])
