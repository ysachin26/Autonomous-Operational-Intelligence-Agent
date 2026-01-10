"""
AOIA ML Engine - Optimization API
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.agents.optimizer_agent import OptimizerAgent

router = APIRouter()
optimizer = OptimizerAgent()


class OptimizationRequest(BaseModel):
    anomalies: List[Dict[str, Any]]
    incidents: Optional[List[Dict[str, Any]]] = None
    current_state: Optional[Dict[str, Any]] = None
    constraints: Optional[Dict[str, Any]] = None


class Recommendation(BaseModel):
    title: str
    description: str
    action_type: str
    priority: str
    estimated_impact: float
    confidence: float
    reasoning: str
    action_payload: Optional[Dict[str, Any]] = None


class OptimizationResponse(BaseModel):
    recommendations: List[Recommendation]
    total_potential_savings: float
    optimization_score: float


class ExecuteRequest(BaseModel):
    recommendation_id: str
    action_type: str
    payload: Optional[Dict[str, Any]] = None


@router.post("/generate", response_model=OptimizationResponse)
async def generate_optimizations(request: OptimizationRequest):
    """
    Generate optimization recommendations based on current anomalies and state.
    """
    result = optimizer.generate_recommendations(
        anomalies=request.anomalies,
        incidents=request.incidents or [],
        current_state=request.current_state or {},
        constraints=request.constraints or {},
    )
    
    return OptimizationResponse(
        recommendations=[Recommendation(**r) for r in result["recommendations"]],
        total_potential_savings=result["total_potential_savings"],
        optimization_score=result["optimization_score"],
    )


@router.post("/execute")
async def execute_recommendation(request: ExecuteRequest):
    """
    Execute an approved recommendation.
    Returns success status and actual impact if measurable.
    """
    result = optimizer.execute(
        recommendation_id=request.recommendation_id,
        action_type=request.action_type,
        payload=request.payload,
    )
    
    return {
        "success": result["success"],
        "message": result["message"],
        "actual_impact": result.get("actual_impact"),
        "execution_details": result.get("details"),
    }


@router.post("/simulate")
async def simulate_optimization(
    action_type: str,
    target: str,
    parameters: Dict[str, Any],
):
    """
    Simulate the effect of an optimization before executing.
    """
    simulation = optimizer.simulate(action_type, target, parameters)
    
    return {
        "action_type": action_type,
        "target": target,
        "simulated_impact": simulation["impact"],
        "risks": simulation["risks"],
        "confidence": simulation["confidence"],
        "recommendation": simulation["recommendation"],
    }


@router.get("/strategies")
async def list_strategies():
    """
    List available optimization strategies.
    """
    return {
        "strategies": [
            {
                "id": "workload_balance",
                "name": "Workload Balancing",
                "description": "Redistribute tasks across resources to minimize bottlenecks",
                "applicable_to": ["OVERLOAD", "IDLE_SPIKE", "THROUGHPUT_DROP"],
            },
            {
                "id": "preventive_maintenance",
                "name": "Preventive Maintenance",
                "description": "Schedule maintenance before failures occur",
                "applicable_to": ["MACHINE_SLOWDOWN", "PATTERN_BREAK"],
            },
            {
                "id": "routing_optimization",
                "name": "Task Routing Optimization",
                "description": "Optimize task assignment and routing logic",
                "applicable_to": ["RESPONSE_DELAY", "THROUGHPUT_DROP"],
            },
            {
                "id": "capacity_planning",
                "name": "Capacity Planning",
                "description": "Proactive resource allocation based on demand forecast",
                "applicable_to": ["OVERLOAD", "THROUGHPUT_DROP"],
            },
            {
                "id": "training_intervention",
                "name": "Training & Skill Development",
                "description": "Identify and address performance gaps through training",
                "applicable_to": ["UNDERPERFORMANCE", "QUALITY_DECLINE"],
            },
        ]
    }
