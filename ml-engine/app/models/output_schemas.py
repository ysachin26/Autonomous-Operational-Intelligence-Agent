"""
AOIA ML Engine - Universal Output Schemas
Domain-agnostic output models for ANY operational workflow.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class SeverityLevel(str, Enum):
    """Severity levels for detections."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ActionStatus(str, Enum):
    """Status of executed actions."""
    PENDING = "pending"
    APPROVED = "approved"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


# ============================================
# UNIVERSAL INEFFICIENCY TYPES
# ============================================

class InefficiencyType(str, Enum):
    """Universal inefficiency types - work across ALL industries."""
    # Time-based
    IDLE_TIME = "IDLE_TIME"                    # Entity not working when should be
    WAIT_TIME = "WAIT_TIME"                    # Work item waiting in queue
    DELAY = "DELAY"                            # Process taking longer than expected
    BOTTLENECK = "BOTTLENECK"                  # Stage causing backup
    
    # Load-based
    OVERLOAD = "OVERLOAD"                      # Entity at/over capacity
    UNDERUTILIZATION = "UNDERUTILIZATION"      # Entity not used enough
    LOAD_IMBALANCE = "LOAD_IMBALANCE"          # Uneven distribution
    
    # Flow-based
    EXCESSIVE_HANDOVERS = "EXCESSIVE_HANDOVERS"  # Too many handoffs
    REWORK = "REWORK"                          # Work being redone
    ESCALATION = "ESCALATION"                  # Excessive escalations
    BOUNCE = "BOUNCE"                          # Work bouncing back
    LOOP = "LOOP"                              # Circular workflow
    
    # SLA-based
    SLA_RISK = "SLA_RISK"                      # At risk of breaching SLA
    SLA_BREACH = "SLA_BREACH"                  # SLA breached
    
    # Throughput-based
    LOW_THROUGHPUT = "LOW_THROUGHPUT"          # Below expected output
    QUEUE_OVERFLOW = "QUEUE_OVERFLOW"          # Queue too large
    
    # State-based
    BLOCKED = "BLOCKED"                        # Entity/work blocked
    OFFLINE = "OFFLINE"                        # Resource unavailable
    
    # Pattern-based
    ANOMALY = "ANOMALY"                        # Statistical anomaly detected
    PATTERN_BREAK = "PATTERN_BREAK"            # Deviation from normal pattern


class InefficiencyDetection(BaseModel):
    """
    Detected operational inefficiency - works across ALL industries.
    
    The location can be any entity: agent, station, team, queue, process stage, etc.
    """
    detection_id: str = Field(...)
    inefficiency_type: str = Field(..., description="Type of inefficiency (see InefficiencyType)")
    
    # WHERE - works for any entity
    location_id: str = Field(..., description="ID of entity/item/process where detected")
    location_type: str = Field(..., description="agent, station, queue, process, work_item, etc.")
    location_name: Optional[str] = Field(None)
    
    # SEVERITY
    severity_score: float = Field(..., ge=0, le=1)
    severity_level: SeverityLevel = Field(...)
    
    # WHEN
    time_window: Dict[str, datetime] = Field(...)
    frequency_pattern: Optional[str] = Field(None, description="one_time, recurring, escalating")
    
    # WHAT
    deviation_percent: float = Field(..., description="Deviation from baseline")
    current_value: Optional[float] = Field(None)
    expected_value: Optional[float] = Field(None)
    
    # IMPACT
    affected_items_count: Optional[int] = Field(0, description="Number of work items affected")
    downstream_impact: Optional[List[str]] = Field(default_factory=list)
    
    # DETAILS
    description: str = Field(...)
    evidence: Optional[List[str]] = Field(default_factory=list)
    
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Legacy compatibility
    @property
    def anomaly_type(self) -> str:
        return self.inefficiency_type
    
    @property
    def anomaly_location(self) -> str:
        return self.location_id


class CausalStep(BaseModel):
    """Single step in a causal chain."""
    step_number: int
    cause: str
    effect: str
    confidence: float = Field(ge=0, le=1)


class RootCauseExplanation(BaseModel):
    """Root cause analysis result - universal across industries."""
    explanation_id: str = Field(...)
    detection_id: str = Field(...)
    
    # Human-readable explanation
    explanation: str = Field(...)
    summary: Optional[str] = Field(None, description="One-line summary")
    
    # Causal analysis
    causal_chain: List[CausalStep] = Field(default_factory=list)
    root_cause_category: Optional[str] = Field(None, description="process, resource, capacity, external, etc.")
    
    # Impact mapping (universal - not just machines!)
    impacted_entities: List[str] = Field(default_factory=list, description="Affected people/systems/stations")
    impacted_work_items: List[str] = Field(default_factory=list, description="Affected tickets/orders/tasks")
    impacted_processes: List[str] = Field(default_factory=list, description="Affected workflows/stages")
    
    # Confidence
    probability_of_correctness: float = Field(..., ge=0, le=1)
    evidence: List[str] = Field(default_factory=list)
    
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Legacy compatibility
    @property
    def impacted_machines(self) -> List[str]:
        return [e for e in self.impacted_entities if 'machine' in e.lower()]
    
    @property
    def impacted_operators(self) -> List[str]:
        return [e for e in self.impacted_entities if any(x in e.lower() for x in ['agent', 'operator', 'employee'])]


class LossBreakdown(BaseModel):
    """Breakdown of financial loss calculation."""
    base_loss: float = Field(0)
    industry_adjustment: float = Field(0)
    severity_adjustment: float = Field(0)
    sla_penalty: Optional[float] = Field(0)
    opportunity_cost: Optional[float] = Field(0)


class FinancialLoss(BaseModel):
    """Financial loss estimation - universal across industries."""
    total_loss: float = Field(...)
    currency: str = Field("INR")
    
    # Per-time metrics
    loss_per_hour: float = Field(0)
    loss_per_day: float = Field(0)
    
    # Projections
    projected_24h_loss: float = Field(0, description="If not fixed in 24 hours")
    projected_weekly_loss: float = Field(0)
    savings_if_fixed: float = Field(0)
    
    # Breakdown
    breakdown: LossBreakdown = Field(...)
    by_type: Dict[str, float] = Field(default_factory=dict)
    by_location: Dict[str, float] = Field(default_factory=dict)
    
    # SLA impact
    sla_breaches: int = Field(0)
    sla_penalties: float = Field(0)
    
    confidence: float = Field(..., ge=0, le=1)
    methodology: str = Field(...)
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Legacy compatibility
    @property
    def money_lost_per_min(self) -> float:
        return self.loss_per_hour / 60
    
    @property
    def money_lost_total(self) -> float:
        return self.total_loss
    
    @property
    def projected_future_loss(self) -> float:
        return self.projected_24h_loss
    
    @property
    def by_source(self) -> Dict[str, float]:
        return self.by_location


# ============================================
# UNIVERSAL ACTION TYPES
# ============================================

class ActionType(str, Enum):
    """Universal action types - work across ALL industries."""
    # Resource actions
    REASSIGN = "REASSIGN"              # Move work to different entity
    REBALANCE_LOAD = "REBALANCE_LOAD"  # Balance workload across entities
    ESCALATE = "ESCALATE"              # Escalate to higher level
    PRIORITIZE = "PRIORITIZE"          # Change priority
    
    # Capacity actions
    ADD_CAPACITY = "ADD_CAPACITY"      # Add more resources
    REDUCE_CAPACITY = "REDUCE_CAPACITY"
    ADJUST_SCHEDULE = "ADJUST_SCHEDULE"
    
    # Process actions
    SKIP_STAGE = "SKIP_STAGE"          # Skip optional stage
    EXPEDITE = "EXPEDITE"              # Fast-track through process
    PAUSE = "PAUSE"                    # Pause processing
    RESUME = "RESUME"                  # Resume processing
    REROUTE = "REROUTE"                # Send to different path
    
    # Alert actions
    ALERT_SUPERVISOR = "ALERT_SUPERVISOR"
    ALERT_TEAM = "ALERT_TEAM"
    SEND_NOTIFICATION = "SEND_NOTIFICATION"
    
    # Maintenance actions (for systems/machines)
    SCHEDULE_MAINTENANCE = "SCHEDULE_MAINTENANCE"
    REQUEST_SUPPORT = "REQUEST_SUPPORT"
    
    # Custom
    CUSTOM = "CUSTOM"


class OptimizationPlan(BaseModel):
    """Generated optimization plan - universal across industries."""
    plan_id: str = Field(...)
    plan_name: Optional[str] = Field(None)
    
    # Recommendations (all optional - use what applies)
    load_rebalancing: Optional[Dict[str, Any]] = Field(None)
    reassignments: Optional[Dict[str, Any]] = Field(None)
    priority_changes: Optional[Dict[str, Any]] = Field(None)
    capacity_adjustments: Optional[Dict[str, Any]] = Field(None)
    process_optimizations: Optional[Dict[str, Any]] = Field(None)
    alerts_to_send: Optional[Dict[str, Any]] = Field(None)
    schedule_changes: Optional[Dict[str, Any]] = Field(None)
    
    # Legacy fields (for backward compatibility)
    shift_adjustment: Optional[Dict[str, Any]] = Field(None)
    maintenance_scheduling: Optional[Dict[str, Any]] = Field(None)
    task_routing: Optional[Dict[str, Any]] = Field(None)
    bottleneck_removal: Optional[Dict[str, Any]] = Field(None)
    priority_modifications: Optional[Dict[str, Any]] = Field(None)
    
    # Impact estimation
    estimated_impact: Dict[str, Any] = Field(default_factory=dict)
    risk_assessment: Dict[str, Any] = Field(default_factory=dict)
    
    # Implementation
    implementation_steps: List[str] = Field(default_factory=list)
    estimated_time_to_implement: Optional[str] = Field(None)
    
    timestamp: datetime = Field(default_factory=datetime.now)


class ExecutionAction(BaseModel):
    """Executed autonomous action - universal across industries."""
    action_id: str = Field(...)
    action_type: str = Field(..., description="See ActionType enum")
    
    # Target
    target_id: str = Field(..., description="ID of entity/item/process targeted")
    target_type: str = Field(..., description="entity, work_item, process, etc.")
    
    # Details
    parameters: Dict[str, Any] = Field(default_factory=dict)
    reason: Optional[str] = Field(None, description="Why this action was taken")
    
    # Status
    status: ActionStatus = Field(default=ActionStatus.PENDING)
    result: Optional[str] = Field(None)
    error: Optional[str] = Field(None)
    
    # Timing
    created_at: datetime = Field(default_factory=datetime.now)
    executed_at: Optional[datetime] = Field(None)
    completed_at: Optional[datetime] = Field(None)
    
    requires_approval: bool = Field(False)
    
    # Legacy compatibility
    @property
    def target(self) -> str:
        return self.target_id


class UpdatedBaselines(BaseModel):
    """Updated baselines from learning."""
    baseline_updates: Dict[str, float] = Field(default_factory=dict)
    threshold_updates: Dict[str, float] = Field(default_factory=dict)
    model_improvements: List[str] = Field(default_factory=list)
    learning_notes: List[str] = Field(default_factory=list)


# ============================================
# UNIFIED AOIA OUTPUT
# ============================================

class AOIAOutput(BaseModel):
    """
    Complete AOIA pipeline output - UNIVERSAL for ANY business workflow.
    
    Works identically whether analyzing:
    - BPO call center agents
    - Retail checkout stations
    - SaaS development sprints
    - Healthcare patient flows
    - Logistics delivery routes
    """
    # Core outputs
    inefficiencies: List[InefficiencyDetection] = Field(default_factory=list)
    root_causes: List[RootCauseExplanation] = Field(default_factory=list)
    financial_loss: Optional[FinancialLoss] = Field(None)
    optimization_plan: Optional[OptimizationPlan] = Field(None)
    actions_executed: List[ExecutionAction] = Field(default_factory=list)
    updated_baselines: Optional[UpdatedBaselines] = Field(None)
    
    # Metadata
    pipeline_id: str = Field(...)
    autonomy_mode: str = Field(...)
    industry: str = Field("GENERAL", description="Industry context")
    processing_time_ms: float = Field(...)
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str = Field("completed")
    errors: List[str] = Field(default_factory=list)
