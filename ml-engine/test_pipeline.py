"""
AOIA Universal Pipeline Test
Tests across MULTIPLE industries - NOT just machines!
"""

from app.orchestrator import AOIAOrchestrator

def test_bpo_scenario():
    """Test BPO call center scenario."""
    print("\n" + "=" * 60)
    print("[BPO] Call Center Scenario")
    print("=" * 60)
    
    o = AOIAOrchestrator()
    
    result = o.run_pipeline({
        "entities": [
            {"entity_id": "agent-101", "entity_type": "agent", "entity_name": "Priya", "state": "busy", "load_percent": 98, "queue_size": 15},
            {"entity_id": "agent-102", "entity_type": "agent", "entity_name": "Raj", "state": "idle", "idle_time_minutes": 25},
            {"entity_id": "agent-103", "entity_type": "agent", "entity_name": "Aisha", "state": "active", "load_percent": 45},
        ],
        "work_items": [
            {"item_id": "TKT-001", "item_type": "ticket", "status": "in_progress", "sla_target_minutes": 60, "sla_remaining_minutes": 8, "handover_count": 4},
            {"item_id": "TKT-002", "item_type": "ticket", "status": "blocked", "rework_count": 3, "bounce_count": 2},
            {"item_id": "TKT-003", "item_type": "ticket", "status": "pending", "wait_time_minutes": 45},
        ],
        "business": {
            "industry": "BPO",
            "baseline_resolution_time_minutes": 30,
            "cost_per_hour": 100,
            "penalty_per_sla_breach": 500
        },
        "autonomy_mode": "FULL_AUTO"
    })
    
    print_results(result)
    return result


def test_retail_scenario():
    """Test retail operations scenario."""
    print("\n" + "=" * 60)
    print("[RETAIL] Operations Scenario")
    print("=" * 60)
    
    o = AOIAOrchestrator()
    
    result = o.run_pipeline({
        "entities": [
            {"entity_id": "cashier-1", "entity_type": "station", "entity_name": "Counter 1", "state": "active", "queue_size": 12},
            {"entity_id": "cashier-2", "entity_type": "station", "entity_name": "Counter 2", "state": "offline"},
            {"entity_id": "floor-staff-1", "entity_type": "employee", "entity_name": "Mike", "load_percent": 30},
        ],
        "work_items": [
            {"item_id": "ORD-501", "item_type": "order", "status": "pending", "wait_time_minutes": 35},
            {"item_id": "RESTOCK-12", "item_type": "task", "status": "blocked", "item_name": "Shelf Restock Aisle 5"},
        ],
        "business": {
            "industry": "RETAIL",
            "cost_per_hour": 50,
        },
        "autonomy_mode": "FULL_AUTO"
    })
    
    print_results(result)
    return result


def test_saas_scenario():
    """Test SaaS development team scenario."""
    print("\n" + "=" * 60)
    print("[SAAS] Development Team Scenario")
    print("=" * 60)
    
    o = AOIAOrchestrator()
    
    result = o.run_pipeline({
        "entities": [
            {"entity_id": "dev-team-a", "entity_type": "team", "entity_name": "Backend Team", "load_percent": 95},
            {"entity_id": "dev-team-b", "entity_type": "team", "entity_name": "Frontend Team", "load_percent": 40},
            {"entity_id": "qa-team", "entity_type": "team", "entity_name": "QA Team", "queue_size": 18},
        ],
        "work_items": [
            {"item_id": "FEAT-101", "item_type": "project", "item_name": "Payment Integration", "handover_count": 5, "rework_count": 4},
            {"item_id": "BUG-234", "item_type": "ticket", "status": "in_progress", "escalation_count": 3},
        ],
        "processes": [
            {"process_id": "sprint-flow", "process_name": "Sprint Workflow", "bottleneck_stage": "QA Review"},
        ],
        "business": {
            "industry": "SAAS",
            "cost_per_hour": 200,
        },
        "autonomy_mode": "FULL_AUTO"
    })
    
    print_results(result)
    return result


def test_healthcare_scenario():
    """Test healthcare patient flow scenario."""
    print("\n" + "=" * 60)
    print("[HEALTHCARE] Patient Flow Scenario")
    print("=" * 60)
    
    o = AOIAOrchestrator()
    
    result = o.run_pipeline({
        "entities": [
            {"entity_id": "nurse-1", "entity_type": "operator", "entity_name": "Nurse Sarah", "load_percent": 92},
            {"entity_id": "dr-patel", "entity_type": "operator", "entity_name": "Dr. Patel", "state": "busy", "queue_size": 8},
            {"entity_id": "lab-station", "entity_type": "station", "entity_name": "Lab Processing", "state": "active", "queue_size": 15},
        ],
        "work_items": [
            {"item_id": "PAT-001", "item_type": "case", "item_name": "Patient John", "wait_time_minutes": 60, "status": "pending"},
            {"item_id": "TEST-123", "item_type": "task", "item_name": "Blood Work", "handover_count": 4},
        ],
        "business": {
            "industry": "HEALTHCARE",
            "cost_per_hour": 150,
        },
        "autonomy_mode": "FULL_AUTO"
    })
    
    print_results(result)
    return result


def test_legacy_format():
    """Test backward compatibility with legacy machine/shift format."""
    print("\n" + "=" * 60)
    print("[LEGACY] Manufacturing Format (Backward Compatibility)")
    print("=" * 60)
    
    o = AOIAOrchestrator()
    
    result = o.run_pipeline({
        "machines": [
            {"machine_id": "M1", "machine_state": "idle", "output_per_min": 6},
            {"machine_id": "M2", "machine_state": "down", "output_per_min": 0}
        ],
        "workflows": [
            {"task_id": "T1", "task_duration": 30, "rework_loops": 3}
        ],
        "shifts": [
            {"operator_id": "OP1", "operator_load": 95}
        ],
        "business": {
            "industry": "MANUFACTURING",
            "baseline_output_per_min": 10,
            "cost_per_min": 75
        }
    })
    
    print_results(result)
    return result


def print_results(result):
    """Print formatted results."""
    print(f"\n[RESULT] Pipeline: {result.pipeline_id}")
    print(f"  Industry: {result.industry}")
    print(f"  Mode: {result.autonomy_mode}")
    print(f"  Status: {result.status}")
    print(f"  Time: {result.processing_time_ms:.0f}ms")
    
    print(f"\n[DETECTIONS] Inefficiencies Found: {len(result.inefficiencies)}")
    for d in result.inefficiencies[:5]:
        print(f"  [{d.severity_level.value.upper()}] {d.inefficiency_type}")
        print(f"      Location: {d.location_type} - {d.location_id}")
        desc = d.description[:70] + "..." if len(d.description) > 70 else d.description
        print(f"      {desc}")
    
    print(f"\n[ROOT CAUSES] Count: {len(result.root_causes)}")
    for rc in result.root_causes[:3]:
        print(f"  * {rc.summary}")
        exp = rc.explanation[:70] + "..." if len(rc.explanation) > 70 else rc.explanation
        print(f"    {exp}")
    
    if result.financial_loss:
        print(f"\n[FINANCIAL IMPACT]")
        print(f"  Total Loss: {result.financial_loss.currency} {result.financial_loss.total_loss:,.0f}")
        print(f"  Loss/Hour: {result.financial_loss.currency} {result.financial_loss.loss_per_hour:,.0f}")
        print(f"  24h Projection: {result.financial_loss.currency} {result.financial_loss.projected_24h_loss:,.0f}")
        print(f"  Savings Potential: {result.financial_loss.currency} {result.financial_loss.savings_if_fixed:,.0f}")
    
    print(f"\n[ACTIONS] Executed: {len(result.actions_executed)}")
    for a in result.actions_executed:
        print(f"  [{a.status.value.upper()}] {a.action_type} -> {a.target_id}")
        print(f"      Reason: {a.reason}")
    
    if result.errors:
        print(f"\n[ERRORS] {result.errors}")


def main():
    print("\n" + "=" * 70)
    print("AOIA UNIVERSAL PIPELINE TEST")
    print("Works for ANY industry - NOT just machines!")
    print("=" * 70)
    
    # Test multiple industries
    test_bpo_scenario()
    test_retail_scenario()
    test_saas_scenario()
    test_healthcare_scenario()
    test_legacy_format()
    
    print("\n" + "=" * 70)
    print("[SUCCESS] All industry tests completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
