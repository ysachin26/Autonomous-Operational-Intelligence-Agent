"""
AOIA ML Engine - Pipeline API
Unified endpoint for running the AOIA autonomous pipeline.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.orchestrator import AOIAOrchestrator, AutonomyMode
from app.models.input_schemas import AOIAInput
from app.models.output_schemas import AOIAOutput


router = APIRouter(prefix="/pipeline", tags=["pipeline"])

# Global orchestrator instance
orchestrator = AOIAOrchestrator()


class ModeChangeRequest(BaseModel):
    """Request to change autonomy mode."""
    mode: str


class PipelineStatusResponse(BaseModel):
    """Pipeline status response."""
    pipeline_id: Optional[str]
    mode: str
    agents: Dict[str, Any]


@router.post("/run", response_model=AOIAOutput)
async def run_pipeline(input_data: AOIAInput) -> AOIAOutput:
    """
    Run the complete AOIA autonomous pipeline.
    
    Pipeline Flow:
    1. Data ingestion & normalization
    2. Detection Agent: Flag anomalies
    3. Knowledge Graph Agent: Map dependencies  
    4. Reasoning Agent: Explain root causes
    5. Loss Estimation Agent: Calculate financial impact
    6. Optimizer Agent: Generate optimization plan
    7. Execution (if mode allows): Perform actions
    8. Learn: Update baselines
    
    The pipeline respects the current autonomy mode:
    - ASSIST: Detection + recommendations only
    - COPILOT: Asks for approval before execution
    - FULL_AUTO: Complete autonomous operation
    
    Returns the unified AOIAOutput with:
    - inefficiencies: Detected anomalies
    - root_causes: Explanations with causal chains
    - financial_loss: Monetary impact
    - optimization_plan: Recommended actions
    - actions_executed: Execution results
    - updated_baselines: Learning updates
    """
    try:
        result = orchestrator.run_pipeline(
            input_data=input_data.model_dump(),
            dry_run=input_data.dry_run or False
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mode")
async def set_mode(request: ModeChangeRequest) -> Dict[str, Any]:
    """
    Set the AOIA autonomy mode.
    
    Modes:
    - ASSIST: Detection + Explanation + Recommendation only (no execution)
    - COPILOT: Asks for approval before executing actions
    - FULL_AUTO: Complete autonomous operation
    """
    return orchestrator.set_mode(request.mode)


@router.get("/mode")
async def get_mode() -> Dict[str, Any]:
    """Get current autonomy mode."""
    mode = orchestrator.mode
    return {
        "mode": mode.value,
        "description": {
            "ASSIST": "Detection and recommendations only",
            "COPILOT": "Requires approval before execution",
            "FULL_AUTO": "Fully autonomous operation"
        }.get(mode.value, "Unknown")
    }


@router.get("/status")
async def get_status() -> Dict[str, Any]:
    """
    Get current pipeline and agent status.
    
    Returns status of all 5 agents and orchestrator state.
    """
    return orchestrator.get_status()


@router.post("/approve/{action_id}")
async def approve_action(action_id: str) -> Dict[str, Any]:
    """
    Approve a pending action (for COPILOT mode).
    
    When in COPILOT mode, actions are created with PENDING status
    and require approval before execution.
    """
    # In a full implementation, this would trigger the pending action
    return {
        "action_id": action_id,
        "status": "approved",
        "message": "Action approved and queued for execution"
    }
