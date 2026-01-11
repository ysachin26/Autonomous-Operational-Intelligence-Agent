"""
AOIA ML Engine - Universal Input Schemas
Domain-agnostic Pydantic models for ANY operational workflow.
Works across: BPO, SaaS, Retail, Healthcare, Logistics, Agencies, HR, Finance, etc.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum


# ============================================
# UNIVERSAL ENTITY TYPES
# ============================================

class EntityType(str, Enum):
    """Universal entity types that work across all industries."""
    # People
    AGENT = "agent"           # BPO agent, support rep, sales rep
    OPERATOR = "operator"     # Factory operator, machine operator
    EMPLOYEE = "employee"     # General staff member
    TEAM = "team"             # A team or department
    
    # Resources
    MACHINE = "machine"       # Physical machine, equipment
    SYSTEM = "system"         # Software system, platform
    STATION = "station"       # Workstation, desk, counter
    CHANNEL = "channel"       # Support channel, sales channel
    
    # Work Items
    TASK = "task"             # Any work item
    TICKET = "ticket"         # Support ticket, service request
    ORDER = "order"           # Sales order, work order
    PROJECT = "project"       # Project, campaign
    CASE = "case"             # Case, file, record
    
    # Locations
    ZONE = "zone"             # Physical or logical zone
    QUEUE = "queue"           # Any waiting queue
    
    # Custom
    CUSTOM = "custom"         # User-defined entity type


class EntityState(str, Enum):
    """Universal states applicable to any entity."""
    ACTIVE = "active"         # Working, processing
    IDLE = "idle"             # Waiting, not working
    BUSY = "busy"             # At capacity
    PAUSED = "paused"         # Temporarily stopped
    BLOCKED = "blocked"       # Cannot proceed
    COMPLETED = "completed"   # Finished
    FAILED = "failed"         # Error state
    OFFLINE = "offline"       # Not available
    AVAILABLE = "available"   # Ready for work


# ============================================
# CORE INPUT MODELS (DOMAIN-AGNOSTIC)
# ============================================

class EntityInput(BaseModel):
    """
    Universal entity input - works for ANY operational entity.
    
    Examples:
    - BPO: {"entity_id": "agent-42", "entity_type": "agent", "state": "busy", "load_percent": 95}
    - Retail: {"entity_id": "cashier-3", "entity_type": "station", "state": "active", "throughput": 12}
    - SaaS: {"entity_id": "dev-team-A", "entity_type": "team", "load_percent": 80}
    """
    entity_id: str = Field(..., description="Unique identifier for the entity")
    entity_type: EntityType = Field(default=EntityType.CUSTOM)
    entity_name: Optional[str] = Field(None, description="Human-readable name")
    state: EntityState = Field(default=EntityState.ACTIVE)
    
    # Universal metrics (use what applies)
    load_percent: Optional[float] = Field(None, ge=0, le=100, description="Current load/utilization %")
    throughput: Optional[float] = Field(None, description="Output rate per time unit")
    capacity: Optional[float] = Field(None, description="Maximum capacity")
    queue_size: Optional[int] = Field(None, description="Items waiting in queue")
    
    # Time tracking
    idle_time_minutes: Optional[float] = Field(0, description="Idle time in minutes")
    active_time_minutes: Optional[float] = Field(0, description="Active time in minutes")
    wait_time_minutes: Optional[float] = Field(0, description="Time spent waiting")
    
    # Relationships
    assigned_to: Optional[List[str]] = Field(default_factory=list, description="Tasks/tickets assigned")
    belongs_to: Optional[str] = Field(None, description="Parent team/department/zone")
    
    # Industry-specific extensions
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)


class WorkItemInput(BaseModel):
    """
    Universal work item - tasks, tickets, orders, cases, projects.
    
    Examples:
    - BPO: {"item_id": "TKT-1234", "item_type": "ticket", "status": "in_progress", "sla_remaining_mins": 30}
    - Retail: {"item_id": "ORD-5678", "item_type": "order", "duration_minutes": 15, "handover_count": 2}
    - Agency: {"item_id": "CAMP-01", "item_type": "project", "rework_count": 3}
    """
    item_id: str = Field(..., description="Unique work item identifier")
    item_type: str = Field("task", description="Type: task, ticket, order, case, project, etc.")
    item_name: Optional[str] = Field(None)
    
    # Status
    status: Optional[str] = Field("pending", description="pending, in_progress, completed, blocked, etc.")
    priority: Optional[str] = Field("normal", description="low, normal, high, urgent, critical")
    
    # Timing
    created_at: Optional[datetime] = Field(None)
    started_at: Optional[datetime] = Field(None)
    completed_at: Optional[datetime] = Field(None)
    due_at: Optional[datetime] = Field(None)
    duration_minutes: Optional[float] = Field(None, description="Time spent on this item")
    wait_time_minutes: Optional[float] = Field(None, description="Time item waited before processing")
    
    # SLA (Service Level Agreement)
    sla_target_minutes: Optional[float] = Field(None, description="Target time to complete")
    sla_remaining_minutes: Optional[float] = Field(None, description="Time left before SLA breach")
    sla_breached: Optional[bool] = Field(False)
    
    # Workflow metrics
    handover_count: Optional[int] = Field(0, description="Number of handoffs between entities")
    rework_count: Optional[int] = Field(0, description="Number of times reworked/revised")
    escalation_count: Optional[int] = Field(0, description="Number of escalations")
    bounce_count: Optional[int] = Field(0, description="Times bounced back (BPO term)")
    
    # Assignments
    assigned_to: Optional[str] = Field(None, description="Current assignee entity_id")
    previous_assignees: Optional[List[str]] = Field(default_factory=list)
    
    # Process flow
    current_stage: Optional[str] = Field(None, description="Current workflow stage")
    process_steps: Optional[List[str]] = Field(default_factory=list, description="Steps taken")
    
    # Value (for financial calculations)
    value: Optional[float] = Field(None, description="Monetary value of this item")
    cost_per_minute: Optional[float] = Field(None, description="Cost per minute for this item type")
    
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ProcessInput(BaseModel):
    """
    Universal process/workflow definition.
    
    Examples:
    - BPO: {"process_id": "ticket-resolution", "stages": ["triage", "investigation", "resolution", "closure"]}
    - HR: {"process_id": "onboarding", "stages": ["offer", "docs", "training", "deployment"]}
    """
    process_id: str = Field(...)
    process_name: Optional[str] = Field(None)
    stages: Optional[List[str]] = Field(default_factory=list, description="Ordered workflow stages")
    expected_duration_minutes: Optional[float] = Field(None)
    sla_target_minutes: Optional[float] = Field(None)
    
    # Current state
    active_items_count: Optional[int] = Field(0)
    bottleneck_stage: Optional[str] = Field(None, description="Current bottleneck stage if any")
    
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class OperationalEvent(BaseModel):
    """
    Universal timestamped operation event.
    
    Examples:
    - "ticket assigned", "task completed", "escalation triggered"
    - "shift started", "break taken", "queue overflow"
    """
    event_id: str = Field(...)
    event_type: str = Field(..., description="Type of event")
    
    # What happened
    source_entity: Optional[str] = Field(None, description="Entity that caused/owns this event")
    target_entity: Optional[str] = Field(None, description="Entity affected by this event")
    work_item_id: Optional[str] = Field(None, description="Related work item if any")
    
    # When
    timestamp: datetime = Field(default_factory=datetime.now)
    duration_minutes: Optional[float] = Field(None)
    
    # Details
    old_value: Optional[Any] = Field(None)
    new_value: Optional[Any] = Field(None)
    description: Optional[str] = Field(None)
    
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class BusinessContext(BaseModel):
    """
    Business parameters for loss calculations and optimization.
    
    Works for ANY industry - just provide what's relevant.
    """
    # Industry identification
    industry: Optional[str] = Field("GENERAL", description="BPO, RETAIL, SAAS, HEALTHCARE, LOGISTICS, etc.")
    department: Optional[str] = Field(None)
    
    # Baselines (expected performance)
    baseline_throughput: Optional[float] = Field(None, description="Expected output per hour")
    baseline_items_per_hour: Optional[float] = Field(None)
    baseline_response_time_minutes: Optional[float] = Field(None)
    baseline_resolution_time_minutes: Optional[float] = Field(None)
    
    # Costs
    cost_per_hour: Optional[float] = Field(75.0, description="Operational cost per hour")
    cost_per_item: Optional[float] = Field(None, description="Cost per work item")
    revenue_per_item: Optional[float] = Field(None, description="Revenue per work item")
    penalty_per_sla_breach: Optional[float] = Field(None)
    
    # SLA thresholds
    sla_thresholds: Optional[Dict[str, float]] = Field(default_factory=dict)
    
    # Resource constraints
    available_capacity: Optional[Dict[str, int]] = Field(default_factory=dict)
    working_hours_per_day: Optional[float] = Field(8.0)
    
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


# ============================================
# UNIFIED AOIA INPUT
# ============================================

class AOIAInput(BaseModel):
    """
    Complete AOIA pipeline input - UNIVERSAL for ANY business workflow.
    
    Use what applies to your industry:
    - entities: People, machines, systems, stations, channels
    - work_items: Tasks, tickets, orders, cases, projects
    - processes: Workflow definitions
    - events: Operational events
    - business: Context and baselines
    """
    # Core operational data
    entities: Optional[List[EntityInput]] = Field(default_factory=list, description="People, machines, systems, stations")
    work_items: Optional[List[WorkItemInput]] = Field(default_factory=list, description="Tasks, tickets, orders, cases")
    processes: Optional[List[ProcessInput]] = Field(default_factory=list, description="Workflow definitions")
    events: Optional[List[OperationalEvent]] = Field(default_factory=list, description="Operational events")
    
    # Business context
    business: Optional[BusinessContext] = Field(None)
    
    # Pipeline control
    autonomy_mode: Optional[str] = Field("FULL_AUTO", description="ASSIST, COPILOT, or FULL_AUTO")
    dry_run: Optional[bool] = Field(False, description="If true, don't execute actions")
    
    class Config:
        json_schema_extra = {
            "example": {
                "entities": [
                    {"entity_id": "agent-1", "entity_type": "agent", "state": "busy", "load_percent": 95},
                    {"entity_id": "agent-2", "entity_type": "agent", "state": "idle", "idle_time_minutes": 20}
                ],
                "work_items": [
                    {"item_id": "TKT-001", "item_type": "ticket", "status": "in_progress", "handover_count": 3, "rework_count": 2}
                ],
                "business": {
                    "industry": "BPO",
                    "baseline_resolution_time_minutes": 30,
                    "cost_per_hour": 100,
                    "penalty_per_sla_breach": 500
                },
                "autonomy_mode": "FULL_AUTO"
            }
        }


# ============================================
# LEGACY COMPATIBILITY (optional use)
# ============================================

# These exist for backward compatibility but EntityInput/WorkItemInput are preferred

class MachineInput(EntityInput):
    """Legacy alias - use EntityInput with entity_type='machine'."""
    machine_id: Optional[str] = Field(None)
    machine_state: Optional[str] = Field(None)
    output_per_min: Optional[float] = Field(None)
    cycle_time: Optional[float] = Field(None)
    
    def __init__(self, **data):
        if 'machine_id' in data:
            data['entity_id'] = data.pop('machine_id')
        if 'machine_state' in data:
            data['state'] = EntityState(data.pop('machine_state'))
        if 'output_per_min' in data:
            data['throughput'] = data.pop('output_per_min')
        data['entity_type'] = EntityType.MACHINE
        super().__init__(**data)


class WorkflowInput(WorkItemInput):
    """Legacy alias - use WorkItemInput."""
    task_id: Optional[str] = Field(None)
    task_duration: Optional[float] = Field(None)
    rework_loops: Optional[int] = Field(None)
    
    def __init__(self, **data):
        if 'task_id' in data:
            data['item_id'] = data.pop('task_id')
        if 'task_duration' in data:
            data['duration_minutes'] = data.pop('task_duration')
        if 'rework_loops' in data:
            data['rework_count'] = data.pop('rework_loops')
        data['item_type'] = 'task'
        super().__init__(**data)


class ShiftInput(EntityInput):
    """Legacy alias - use EntityInput with entity_type='operator' or 'agent'."""
    operator_id: Optional[str] = Field(None)
    operator_load: Optional[float] = Field(None)
    
    def __init__(self, **data):
        if 'operator_id' in data:
            data['entity_id'] = data.pop('operator_id')
        if 'operator_load' in data:
            data['load_percent'] = data.pop('operator_load')
        data['entity_type'] = EntityType.OPERATOR
        super().__init__(**data)


class BusinessInput(BusinessContext):
    """Legacy alias - use BusinessContext."""
    baseline_output_per_min: Optional[float] = Field(None)
    cost_per_min: Optional[float] = Field(None)
    
    def __init__(self, **data):
        if 'baseline_output_per_min' in data:
            data['baseline_throughput'] = data.pop('baseline_output_per_min') * 60
        if 'cost_per_min' in data:
            data['cost_per_hour'] = data.pop('cost_per_min') * 60
        super().__init__(**data)
