"""
AOIA ML Engine - Data Models
Pydantic schemas for input/output data structures.
"""

from app.models.input_schemas import (
    MachineInput,
    WorkflowInput,
    ShiftInput,
    BusinessInput,
    OperationalEvent,
    AOIAInput,
)

from app.models.output_schemas import (
    InefficiencyDetection,
    RootCauseExplanation,
    FinancialLoss,
    OptimizationPlan,
    ExecutionAction,
    AOIAOutput,
)

__all__ = [
    # Inputs
    "MachineInput",
    "WorkflowInput", 
    "ShiftInput",
    "BusinessInput",
    "OperationalEvent",
    "AOIAInput",
    # Outputs
    "InefficiencyDetection",
    "RootCauseExplanation",
    "FinancialLoss",
    "OptimizationPlan",
    "ExecutionAction",
    "AOIAOutput",
]
