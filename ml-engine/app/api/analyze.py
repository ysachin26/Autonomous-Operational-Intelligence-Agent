"""
AOIA ML Engine - Analysis API (Loss Calculation & Root Cause)
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.services.loss_calculator import LossCalculator
from app.services.root_cause_analyzer import RootCauseAnalyzer

router = APIRouter()
loss_calc = LossCalculator()
rca = RootCauseAnalyzer()


class LossRequest(BaseModel):
    anomaly_type: str
    source: str
    duration_minutes: float
    deviation_percent: float
    cost_per_minute: float = 75.0
    industry: str = "MANUFACTURING"


class LossResponse(BaseModel):
    estimated_loss: float
    currency: str
    breakdown: Dict[str, float]
    confidence: float
    methodology: str


class RootCauseRequest(BaseModel):
    anomaly_type: str
    source: str
    value: float
    expected_value: float
    timestamp: str
    context: Optional[Dict[str, Any]] = None


class RootCauseResponse(BaseModel):
    primary_cause: str
    confidence: float
    contributing_factors: List[str]
    evidence: List[str]
    recommended_actions: List[str]


@router.post("/loss", response_model=LossResponse)
async def calculate_loss(request: LossRequest):
    """
    Calculate monetary loss from an operational inefficiency.
    
    Formula: loss = (expected_output - actual_output) × cost_per_minute × duration
    """
    result = loss_calc.calculate(
        anomaly_type=request.anomaly_type,
        source=request.source,
        duration_minutes=request.duration_minutes,
        deviation_percent=request.deviation_percent,
        cost_per_minute=request.cost_per_minute,
        industry=request.industry,
    )
    
    return LossResponse(**result)


@router.post("/root-cause", response_model=RootCauseResponse)
async def analyze_root_cause(request: RootCauseRequest):
    """
    Perform root cause analysis using AI reasoning.
    """
    result = rca.analyze(
        anomaly_type=request.anomaly_type,
        source=request.source,
        value=request.value,
        expected_value=request.expected_value,
        timestamp=request.timestamp,
        context=request.context,
    )
    
    return RootCauseResponse(**result)


@router.post("/impact-assessment")
async def assess_impact(
    anomalies: List[Dict[str, Any]],
    time_range_hours: int = 24,
    cost_per_minute: float = 75.0,
):
    """
    Assess the total impact of multiple anomalies over a time period.
    """
    total_loss = 0
    by_type = {}
    by_source = {}
    
    for anomaly in anomalies:
        loss = loss_calc.calculate(
            anomaly_type=anomaly.get("anomaly_type", "UNKNOWN"),
            source=anomaly.get("source", "unknown"),
            duration_minutes=anomaly.get("duration_minutes", 30),
            deviation_percent=anomaly.get("deviation_percent", 10),
            cost_per_minute=cost_per_minute,
            industry="MANUFACTURING",
        )
        
        loss_amount = loss["estimated_loss"]
        total_loss += loss_amount
        
        atype = anomaly.get("anomaly_type", "UNKNOWN")
        source = anomaly.get("source", "unknown")
        
        by_type[atype] = by_type.get(atype, 0) + loss_amount
        by_source[source] = by_source.get(source, 0) + loss_amount
    
    return {
        "time_range_hours": time_range_hours,
        "total_loss": round(total_loss, 2),
        "currency": "INR",
        "anomaly_count": len(anomalies),
        "by_type": {k: round(v, 2) for k, v in sorted(by_type.items(), key=lambda x: -x[1])},
        "by_source": {k: round(v, 2) for k, v in sorted(by_source.items(), key=lambda x: -x[1])},
        "top_contributor": max(by_source.items(), key=lambda x: x[1])[0] if by_source else None,
    }
