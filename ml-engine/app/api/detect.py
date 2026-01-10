"""
AOIA ML Engine - Anomaly Detection API
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
from app.services.anomaly_detector import AnomalyDetector

router = APIRouter()
detector = AnomalyDetector()


class MetricData(BaseModel):
    timestamp: str
    value: float
    source: str
    metric_type: str


class DetectionRequest(BaseModel):
    metrics: List[MetricData]
    sensitivity: float = 0.8  # 0-1, higher = more sensitive


class AnomalyResult(BaseModel):
    is_anomaly: bool
    score: float
    severity: str
    description: str
    expected_value: float
    deviation_percent: float
    metric: MetricData


class DetectionResponse(BaseModel):
    total_analyzed: int
    anomalies_found: int
    results: List[AnomalyResult]


@router.post("/batch", response_model=DetectionResponse)
async def detect_anomalies_batch(request: DetectionRequest):
    """
    Detect anomalies in a batch of metrics using Isolation Forest.
    """
    if not request.metrics:
        raise HTTPException(status_code=400, detail="No metrics provided")
    
    results = detector.detect_batch(request.metrics, request.sensitivity)
    
    anomalies = [r for r in results if r["is_anomaly"]]
    
    return DetectionResponse(
        total_analyzed=len(request.metrics),
        anomalies_found=len(anomalies),
        results=[AnomalyResult(**r) for r in results if r["is_anomaly"]],
    )


@router.post("/realtime")
async def detect_realtime(metric: MetricData, context: Optional[List[float]] = None):
    """
    Real-time single metric anomaly detection.
    Uses recent context for comparison if provided.
    """
    result = detector.detect_single(metric, context or [])
    
    return {
        "is_anomaly": result["is_anomaly"],
        "score": result["score"],
        "severity": result["severity"],
        "description": result["description"],
        "recommendation": result.get("recommendation", None),
    }


@router.get("/thresholds")
async def get_thresholds():
    """
    Get current anomaly detection thresholds.
    """
    return {
        "utilization": {"low": 40, "high": 95},
        "throughput": {"low": 60, "high": None},
        "idle_time": {"low": None, "high": 20},
        "response_time": {"low": None, "high": 500},
        "quality_score": {"low": 85, "high": None},
    }


@router.post("/train")
async def train_model(metrics: List[MetricData]):
    """
    Train/update the anomaly detection model with new data.
    """
    if len(metrics) < 100:
        raise HTTPException(
            status_code=400, 
            detail="At least 100 data points required for training"
        )
    
    success = detector.train(metrics)
    
    return {
        "success": success,
        "message": "Model trained successfully" if success else "Training failed",
        "samples_used": len(metrics),
    }
