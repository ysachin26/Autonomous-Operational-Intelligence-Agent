"""
AOIA ML Engine - Main Application
Autonomous Operational Intelligence Agent
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.api import router as api_router

load_dotenv()

app = FastAPI(
    title="AOIA ML Engine",
    description="Autonomous Operational Intelligence Agent - ML & AI Services",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGIN", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "name": "AOIA ML Engine",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "detect": "/api/detect",
            "analyze": "/api/analyze",
            "chat": "/api/chat",
            "explain": "/api/explain",
            "optimize": "/api/optimize",
        },
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "anomaly_detector": "operational",
            "loss_calculator": "operational",
            "reasoning_agent": "operational",
            "optimizer": "operational",
        },
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
