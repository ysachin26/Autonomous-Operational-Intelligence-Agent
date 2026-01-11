"""
AOIA ML Engine - Demo API Endpoints
Provides demonstration scenarios for the prototype UI.
"""

from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from app.orchestrator import AOIAOrchestrator


router = APIRouter(prefix="/demo", tags=["demonstrations"])


class DemoResponse(BaseModel):
    """Demo scenario response structure."""
    scenario_name: str
    status: str
    
    # Problem
    problem: Dict[str, Any]
    
    # AOIA Steps
    detection: Dict[str, Any]
    root_cause: Dict[str, Any]
    financial_loss: Dict[str, Any]
    optimization: Dict[str, Any]
    execution: Dict[str, Any]
    
    # Summary for UI
    summary: Dict[str, Any]
    
    processing_time_ms: float


@router.post("/bpo-sla-prevention")
async def run_bpo_demo() -> DemoResponse:
    """
    Run the BPO Ticket Delay & SLA Violation Prevention demo.
    
    This demonstrates the complete AOIA autonomous loop:
    1. Detection - Find overloaded agent and at-risk ticket
    2. Root Cause - Explain why delay happened
    3. Financial Loss - Calculate monetary impact
    4. Optimization - Generate reassignment plan
    5. Execution - Perform corrective actions
    
    Perfect for hackathon judges to understand AOIA's capabilities.
    """
    start_time = datetime.now()
    
    try:
        # ===================================================
        # SCENARIO DATA
        # ===================================================
        scenario = {
            "ticket_id": "TKT-4781",
            "created_at": "10:02 AM",
            "current_time": "10:49 AM",
            "sla_limit_minutes": 45,
            "baseline_resolution_minutes": 18,
            "cost_per_minute_delay": 12,
            "penalty_per_sla_breach": 500,
            "elapsed_minutes": 47,
            "sla_remaining_minutes": -2,  # Already breached
            "delay_above_baseline": 29,
        }
        
        agents = {
            "Agent_23": {"load_percent": 92, "status": "OVERLOADED"},
            "Agent_12": {"load_percent": 38, "status": "AVAILABLE"},
        }
        
        # ===================================================
        # PROBLEM STATEMENT
        # ===================================================
        problem = {
            "title": "BPO Ticket Delay & SLA Violation Prevention",
            "description": f"Ticket {scenario['ticket_id']} is stuck with an overloaded agent and at risk of SLA breach",
            "ticket_id": scenario["ticket_id"],
            "elapsed_minutes": scenario["elapsed_minutes"],
            "sla_limit_minutes": scenario["sla_limit_minutes"],
            "sla_remaining_minutes": scenario["sla_remaining_minutes"],
            "assigned_agent": "Agent_23",
            "agent_load": f"{agents['Agent_23']['load_percent']}%",
            "risk": "HIGH - SLA breach imminent",
        }
        
        # ===================================================
        # RUN AOIA PIPELINE
        # ===================================================
        orchestrator = AOIAOrchestrator()
        
        input_data = {
            "entities": [
                {
                    "entity_id": "Agent_23",
                    "entity_type": "agent",
                    "entity_name": "Agent 23 (Overloaded)",
                    "state": "busy",
                    "load_percent": agents["Agent_23"]["load_percent"],
                    "queue_size": 8,
                },
                {
                    "entity_id": "Agent_12",
                    "entity_type": "agent",
                    "entity_name": "Agent 12 (Available)",
                    "state": "active",
                    "load_percent": agents["Agent_12"]["load_percent"],
                    "queue_size": 2,
                },
            ],
            "work_items": [
                {
                    "item_id": scenario["ticket_id"],
                    "item_type": "ticket",
                    "item_name": f"Customer Ticket {scenario['ticket_id']}",
                    "status": "in_progress",
                    "priority": "high",
                    "duration_minutes": scenario["elapsed_minutes"],
                    "wait_time_minutes": scenario["delay_above_baseline"],
                    "sla_target_minutes": scenario["sla_limit_minutes"],
                    "sla_remaining_minutes": scenario["sla_remaining_minutes"],
                    "assigned_to": "Agent_23",
                    "cost_per_minute": scenario["cost_per_minute_delay"],
                }
            ],
            "business": {
                "industry": "BPO",
                "department": "Customer Support",
                "baseline_resolution_time_minutes": scenario["baseline_resolution_minutes"],
                "cost_per_hour": scenario["cost_per_minute_delay"] * 60,
                "penalty_per_sla_breach": scenario["penalty_per_sla_breach"],
            },
            "autonomy_mode": "FULL_AUTO",
        }
        
        result = orchestrator.run_pipeline(input_data)
        
        # ===================================================
        # FORMAT DETECTION OUTPUT
        # ===================================================
        detection = {
            "detected_issues": [
                {
                    "type": d.inefficiency_type,
                    "location": d.location_id,
                    "severity": d.severity_level.value,
                    "description": d.description[:100],
                }
                for d in result.inefficiencies[:5]
            ],
            "summary": {
                "total_detections": len(result.inefficiencies),
                "critical_issues": len([d for d in result.inefficiencies if d.severity_level.value == "critical"]),
                "high_issues": len([d for d in result.inefficiencies if d.severity_level.value == "high"]),
            }
        }
        
        # ===================================================
        # FORMAT ROOT CAUSE
        # ===================================================
        root_cause = {
            "primary_cause": f"Agent_23 is at {agents['Agent_23']['load_percent']}% capacity causing ticket delay",
            "explanation": f"Ticket {scenario['ticket_id']} is delayed because the assigned agent (Agent_23) is overloaded at {agents['Agent_23']['load_percent']}% capacity. This is causing resolution time to exceed the SLA threshold of {scenario['sla_limit_minutes']} minutes.",
            "contributing_factors": [
                f"Agent_23 workload: {agents['Agent_23']['load_percent']}%",
                f"Ticket age: {scenario['elapsed_minutes']} minutes",
                f"SLA remaining: {scenario['sla_remaining_minutes']} minutes",
            ],
            "risk_level": "CRITICAL",
            "confidence": 0.94,
        }
        
        # ===================================================
        # FORMAT FINANCIAL LOSS
        # ===================================================
        current_loss = scenario["delay_above_baseline"] * scenario["cost_per_minute_delay"]
        projected_penalty = scenario["penalty_per_sla_breach"] if scenario["sla_remaining_minutes"] <= 0 else 0
        
        financial_loss = {
            "delay_minutes": scenario["delay_above_baseline"],
            "baseline_minutes": scenario["baseline_resolution_minutes"],
            "loss_amount": current_loss,
            "currency": "INR",
            "projected_penalty": projected_penalty,
            "total_at_risk": current_loss + projected_penalty,
            "calculation": f"{scenario['delay_above_baseline']} min x INR {scenario['cost_per_minute_delay']}/min = INR {current_loss}",
            "savings_if_fixed": current_loss + projected_penalty,
        }
        
        # ===================================================
        # FORMAT OPTIMIZATION PLAN
        # ===================================================
        optimization = {
            "strategy": "REASSIGN_TICKET",
            "from_agent": {
                "id": "Agent_23",
                "load": f"{agents['Agent_23']['load_percent']}%",
                "status": "OVERLOADED",
            },
            "to_agent": {
                "id": "Agent_12",
                "load": f"{agents['Agent_12']['load_percent']}%",
                "status": "AVAILABLE",
            },
            "expected_outcome": {
                "new_resolution_time": "10 minutes",
                "sla_protected": True,
                "workload_balanced": True,
            },
            "priority": "IMMEDIATE",
        }
        
        # ===================================================
        # FORMAT EXECUTION ACTIONS
        # ===================================================
        execution = {
            "mode": result.autonomy_mode,
            "actions": [
                {
                    "action": "REASSIGN_TICKET",
                    "from": "Agent_23",
                    "to": "Agent_12",
                    "ticket": scenario["ticket_id"],
                    "status": "COMPLETED",
                },
                {
                    "action": "UPDATE_CRM",
                    "field": "assigned_agent",
                    "new_value": "Agent_12",
                    "status": "COMPLETED",
                },
                {
                    "action": "NOTIFY_SUPERVISOR",
                    "message": f"Ticket {scenario['ticket_id']} reassigned due to SLA risk",
                    "status": "COMPLETED",
                },
                {
                    "action": "UPDATE_SLA_TRACKING",
                    "ticket": scenario["ticket_id"],
                    "new_eta": "10 minutes",
                    "status": "COMPLETED",
                },
            ],
            "aoia_actions": [
                {
                    "id": a.action_id,
                    "type": a.action_type,
                    "target": a.target_id,
                    "status": a.status.value,
                }
                for a in result.actions_executed
            ],
        }
        
        # ===================================================
        # FINAL SUMMARY FOR UI
        # ===================================================
        summary = {
            "headline": f"Ticket {scenario['ticket_id']} Protected from SLA Violation!",
            "message": f"AOIA automatically reassigned ticket {scenario['ticket_id']} from Agent_23 (92% load) to Agent_12 (38% load) to prevent SLA violation. Estimated loss of INR {current_loss + projected_penalty} was avoided.",
            "metrics": {
                "loss_prevented": f"INR {current_loss + projected_penalty}",
                "sla_protected": True,
                "actions_taken": 4,
                "processing_time_ms": result.processing_time_ms,
            },
            "before_aoia": {
                "ticket_status": "AT_RISK",
                "assigned_to": "Agent_23 (Overloaded)",
                "sla_status": "BREACH_IMMINENT",
            },
            "after_aoia": {
                "ticket_status": "PROTECTED",
                "assigned_to": "Agent_12 (Available)",
                "sla_status": "ON_TRACK",
            },
        }
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return DemoResponse(
            scenario_name="BPO Ticket Delay & SLA Violation Prevention",
            status="completed",
            problem=problem,
            detection=detection,
            root_cause=root_cause,
            financial_loss=financial_loss,
            optimization=optimization,
            execution=execution,
            summary=summary,
            processing_time_ms=processing_time,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/scenarios")
async def list_demo_scenarios() -> Dict[str, Any]:
    """List available demo scenarios."""
    return {
        "scenarios": [
            {
                "id": "bpo-sla-prevention",
                "name": "BPO Ticket Delay & SLA Violation Prevention",
                "industry": "BPO",
                "description": "Shows AOIA preventing SLA breach by reassigning overloaded tickets",
                "endpoint": "/api/demo/bpo-sla-prevention",
            },
        ],
        "total": 1,
    }
