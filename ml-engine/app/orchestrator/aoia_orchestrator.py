"""
AOIA ML Engine - Universal Orchestrator
Coordinates all agents for ANY operational workflow.

Works across: BPO, SaaS, Retail, Healthcare, Logistics, Agencies, HR, Finance, etc.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
import logging
import json

from app.orchestrator.autonomy_modes import AutonomyMode, ModeConfig
from app.agents.detection_agent import DetectionAgent
from app.agents.knowledge_graph_agent import KnowledgeGraphAgent
from app.agents.loss_estimation_agent import LossEstimationAgent
from app.agents.optimizer_agent import OptimizerAgent
from app.agents.reasoning_agent import ReasoningAgent
from app.models.output_schemas import (
    AOIAOutput, 
    InefficiencyDetection,
    RootCauseExplanation,
    FinancialLoss,
    OptimizationPlan,
    ExecutionAction,
    UpdatedBaselines,
    ActionStatus,
    CausalStep,
    SeverityLevel,
    LossBreakdown,
)


class AOIAOrchestrator:
    """
    AOIA Universal Orchestrator
    
    Works for ANY operational workflow:
    - BPO call centers
    - SaaS development teams
    - Retail operations
    - Healthcare patient flows
    - Logistics networks
    - Agencies and studios
    - HR and finance ops
    
    Pipeline: Data → Detect → Reason → Quantify → Plan → Execute → Learn
    """
    
    def __init__(self):
        self.logger = logging.getLogger("aoia.orchestrator")
        
        # Initialize all agents
        self.detection_agent = DetectionAgent()
        self.knowledge_graph_agent = KnowledgeGraphAgent()
        self.loss_estimation_agent = LossEstimationAgent()
        self.optimizer_agent = OptimizerAgent()
        self.reasoning_agent = ReasoningAgent()
        
        # Current autonomy mode
        self._mode = AutonomyMode.FULL_AUTO
        
        # Pipeline state
        self._pipeline_id: Optional[str] = None
        self._industry: str = "GENERAL"
        
        # Learning/baseline tracking
        self._baselines: Dict[str, float] = {}
        self._thresholds: Dict[str, float] = {}
        self._learning_history: List[Dict[str, Any]] = []
    
    @property
    def mode(self) -> AutonomyMode:
        return self._mode
    
    def set_mode(self, mode: str) -> Dict[str, Any]:
        """Set the autonomy mode."""
        self._mode = AutonomyMode.from_string(mode)
        config = ModeConfig.get_config(self._mode)
        return {
            "mode": self._mode.value,
            "config": config,
            "message": f"Mode set to {self._mode.value}: {config['description']}"
        }
    
    def run_pipeline(
        self, 
        input_data: Dict[str, Any],
        dry_run: bool = False
    ) -> AOIAOutput:
        """
        Run the universal AOIA autonomous pipeline.
        
        Works with ANY operational data - not just machines!
        """
        start_time = datetime.now()
        self._pipeline_id = f"pipeline-{uuid.uuid4().hex[:12]}"
        errors: List[str] = []
        
        # Extract settings
        mode_str = input_data.get("autonomy_mode", self._mode.value)
        self._mode = AutonomyMode.from_string(mode_str)
        
        business = input_data.get("business", {})
        self._industry = business.get("industry", "GENERAL")
        
        if input_data.get("dry_run"):
            dry_run = True
        
        self.logger.info(f"Starting pipeline {self._pipeline_id} for {self._industry} in {self._mode.value} mode")
        
        try:
            # ============================================
            # Step 1: Normalize input (support legacy formats)
            # ============================================
            normalized_data = self._normalize_input(input_data)
            
            # ============================================
            # Step 2: Detection Agent - find inefficiencies
            # ============================================
            detection_result = self.detection_agent.process(normalized_data)
            detections = detection_result.get("detections", [])
            
            if detection_result.get("status") == "error":
                errors.append(f"Detection: {detection_result.get('error')}")
            
            # ============================================
            # Step 3: Knowledge Graph Agent - map dependencies
            # ============================================
            kg_result = self.knowledge_graph_agent.process(
                normalized_data,
                context={"detections": detections}
            )
            affected_nodes = kg_result.get("affected_nodes", {})
            
            if kg_result.get("status") == "error":
                errors.append(f"KnowledgeGraph: {kg_result.get('error')}")
            
            # ============================================
            # Step 4: Reasoning Agent - explain root causes
            # ============================================
            root_causes = self._generate_root_causes(detections, affected_nodes)
            
            # ============================================
            # Step 5: Loss Estimation Agent - calculate impact
            # ============================================
            loss_input = {
                "detections": detections,
                "business": normalized_data.get("business", {}),
            }
            loss_result = self.loss_estimation_agent.process(loss_input)
            financial_loss = loss_result.get("financial_loss")
            
            if loss_result.get("status") == "error":
                errors.append(f"LossEstimation: {loss_result.get('error')}")
            
            # ============================================
            # Step 6: Optimizer Agent - generate plan
            # ============================================
            optimization_plan = self._generate_optimization_plan(
                detections, root_causes, financial_loss
            )
            
            # ============================================
            # Step 7: Execution (if mode allows)
            # ============================================
            actions_executed = []
            mode_config = ModeConfig.get_config(self._mode)
            
            if mode_config["can_execute"] and not dry_run:
                if mode_config["requires_approval"]:
                    actions_executed = self._create_pending_actions(optimization_plan, detections)
                else:
                    actions_executed = self._execute_actions(optimization_plan, detections)
            
            # ============================================
            # Step 8: Learn and update baselines
            # ============================================
            updated_baselines = self._learn_from_results(detections, actions_executed)
            
            # Build output
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            output = AOIAOutput(
                inefficiencies=self._convert_to_detections(detections),
                root_causes=root_causes,
                financial_loss=self._convert_to_financial_loss(financial_loss) if financial_loss else None,
                optimization_plan=optimization_plan,
                actions_executed=actions_executed,
                updated_baselines=updated_baselines,
                pipeline_id=self._pipeline_id,
                autonomy_mode=self._mode.value,
                industry=self._industry,
                processing_time_ms=processing_time,
                timestamp=datetime.now(),
                status="completed" if not errors else "completed_with_errors",
                errors=errors,
            )
            
            self.logger.info(f"Pipeline {self._pipeline_id} completed in {processing_time:.0f}ms")
            return output
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return AOIAOutput(
                inefficiencies=[],
                root_causes=[],
                financial_loss=None,
                optimization_plan=None,
                actions_executed=[],
                updated_baselines=None,
                pipeline_id=self._pipeline_id,
                autonomy_mode=self._mode.value,
                industry=self._industry,
                processing_time_ms=processing_time,
                timestamp=datetime.now(),
                status="failed",
                errors=[str(e)],
            )
    
    def _normalize_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize input - support both new universal format and legacy format."""
        # New universal format
        entities = input_data.get("entities", [])
        work_items = input_data.get("work_items", [])
        processes = input_data.get("processes", [])
        events = input_data.get("events", [])
        business = input_data.get("business", {})
        
        # Legacy format support
        machines = input_data.get("machines", [])
        shifts = input_data.get("shifts", [])
        workflows = input_data.get("workflows", [])
        
        # Convert legacy to new format
        for m in machines:
            entities.append({
                "entity_id": m.get("machine_id", m.get("entity_id")),
                "entity_type": "machine",
                "state": m.get("machine_state", m.get("state", "active")),
                "throughput": m.get("output_per_min"),
                "load_percent": m.get("operator_load"),
                **m
            })
        
        for s in shifts:
            entities.append({
                "entity_id": s.get("operator_id", s.get("entity_id")),
                "entity_type": "operator",
                "load_percent": s.get("operator_load"),
                "idle_time_minutes": s.get("idle_time", 0),
                **s
            })
        
        for w in workflows:
            work_items.append({
                "item_id": w.get("task_id", w.get("item_id")),
                "item_type": "task",
                "duration_minutes": w.get("task_duration"),
                "rework_count": w.get("rework_loops", 0),
                "handover_count": w.get("task_transfers", 0),
                **w
            })
        
        # Business defaults
        if not business:
            business = {
                "industry": "GENERAL",
                "cost_per_hour": 75,
            }
        
        # Legacy business format
        if business.get("baseline_output_per_min"):
            business["baseline_throughput"] = business["baseline_output_per_min"] * 60
        if business.get("cost_per_min"):
            business["cost_per_hour"] = business["cost_per_min"] * 60
        
        return {
            "entities": entities,
            "work_items": work_items,
            "processes": processes,
            "events": events,
            "business": business,
        }
    
    def _generate_root_causes(
        self, 
        detections: List[Dict],
        affected_nodes: Dict[str, Any]
    ) -> List[RootCauseExplanation]:
        """Generate root cause explanations - works for any inefficiency type."""
        root_causes = []
        
        for detection in detections:
            detection_id = detection.get("detection_id", "")
            ineff_type = detection.get("inefficiency_type") or detection.get("anomaly_type", "UNKNOWN")
            location = detection.get("location_id") or detection.get("anomaly_location", "unknown")
            location_type = detection.get("location_type", "entity")
            
            # Generate explanation based on inefficiency type
            explanation = self._get_explanation(ineff_type, location, location_type, detection)
            causal_chain = self._build_causal_chain(ineff_type, detection)
            
            # Get impacted items from knowledge graph
            impacted_entities = affected_nodes.get("affected_machines", []) + affected_nodes.get("affected_operators", [])
            impacted_tasks = affected_nodes.get("affected_tasks", [])
            
            root_cause = RootCauseExplanation(
                explanation_id=f"rca-{uuid.uuid4().hex[:8]}",
                detection_id=detection_id,
                explanation=explanation,
                summary=f"{ineff_type} at {location}",
                causal_chain=causal_chain,
                root_cause_category=self._categorize_root_cause(ineff_type),
                impacted_entities=impacted_entities,
                impacted_work_items=impacted_tasks,
                impacted_processes=[],
                probability_of_correctness=self._calculate_probability(detection),
                evidence=self._gather_evidence(detection),
                timestamp=datetime.now(),
            )
            root_causes.append(root_cause)
        
        return root_causes
    
    def _get_explanation(
        self, 
        ineff_type: str, 
        location: str,
        location_type: str,
        detection: Dict
    ) -> str:
        """Generate human-readable explanation for any inefficiency type."""
        explanations = {
            # Time issues
            "IDLE_TIME": f"{location_type.title()} '{location}' is experiencing excessive idle time, likely due to waiting for work, unclear assignments, or upstream delays.",
            "WAIT_TIME": f"Work item at '{location}' has been waiting too long, indicating queue buildup or resource unavailability.",
            "DELAY": f"Processing at '{location}' is taking longer than expected, suggesting capacity issues or process complexity.",
            "BOTTLENECK": f"Stage '{location}' is a bottleneck causing upstream backup. Work is arriving faster than it can be processed.",
            
            # Load issues
            "OVERLOAD": f"{location_type.title()} '{location}' is overloaded and at risk of burnout, errors, or delays. Immediate load redistribution recommended.",
            "UNDERUTILIZATION": f"{location_type.title()} '{location}' is underutilized. Consider reassigning work to improve efficiency.",
            "LOAD_IMBALANCE": f"Significant load imbalance detected across the system. Some resources are overworked while others are idle.",
            
            # Flow issues
            "EXCESSIVE_HANDOVERS": f"Work at '{location}' has too many handoffs between people/teams, causing delays and potential communication gaps.",
            "REWORK": f"Work at '{location}' is requiring multiple revisions, indicating quality issues or unclear requirements.",
            "ESCALATION": f"Work at '{location}' has been escalated multiple times, suggesting complexity or skill gaps.",
            "BOUNCE": f"Work at '{location}' keeps bouncing back, indicating process or assignment issues.",
            
            # SLA issues
            "SLA_RISK": f"Work at '{location}' is at risk of breaching SLA. Immediate attention required to meet commitment.",
            "SLA_BREACH": f"SLA has been BREACHED at '{location}'. This may result in penalties and customer dissatisfaction.",
            
            # Throughput/Queue
            "LOW_THROUGHPUT": f"{location_type.title()} '{location}' has below-expected output, indicating efficiency issues.",
            "QUEUE_OVERFLOW": f"Queue at '{location}' is overflowing. Capacity increase or redistribution needed.",
            
            # State issues
            "BLOCKED": f"{location_type.title()} '{location}' is blocked and cannot proceed. Investigation required.",
            "OFFLINE": f"{location_type.title()} '{location}' is offline/unavailable, impacting capacity.",
        }
        
        return explanations.get(
            ineff_type,
            f"Inefficiency detected at {location_type} '{location}': {ineff_type}. Investigation recommended."
        )
    
    def _build_causal_chain(self, ineff_type: str, detection: Dict) -> List[CausalStep]:
        """Build causal chain for any inefficiency type."""
        chains = {
            "OVERLOAD": [
                CausalStep(step_number=1, cause="High work assignment", effect="Resource at capacity", confidence=0.9),
                CausalStep(step_number=2, cause="Over-capacity operation", effect="Quality/speed degradation", confidence=0.85),
                CausalStep(step_number=3, cause="Degraded performance", effect="SLA risk and potential burnout", confidence=0.8),
            ],
            "IDLE_TIME": [
                CausalStep(step_number=1, cause="No work assigned or waiting for input", effect="Resource idle", confidence=0.85),
                CausalStep(step_number=2, cause="Idle time", effect="Wasted capacity and cost", confidence=0.9),
            ],
            "REWORK": [
                CausalStep(step_number=1, cause="Quality issue or unclear requirements", effect="Work rejected/returned", confidence=0.85),
                CausalStep(step_number=2, cause="Rework required", effect="Time and cost increase", confidence=0.9),
                CausalStep(step_number=3, cause="Repeated rework", effect="SLA risk and frustration", confidence=0.8),
            ],
            "SLA_BREACH": [
                CausalStep(step_number=1, cause="Delayed processing or insufficient capacity", effect="SLA deadline missed", confidence=0.95),
                CausalStep(step_number=2, cause="SLA breach", effect="Penalty and customer dissatisfaction", confidence=0.9),
            ],
            "BOTTLENECK": [
                CausalStep(step_number=1, cause="Stage capacity insufficient", effect="Work queues up", confidence=0.9),
                CausalStep(step_number=2, cause="Queue buildup", effect="Overall flow slows down", confidence=0.85),
                CausalStep(step_number=3, cause="Slow flow", effect="End-to-end delays", confidence=0.8),
            ],
        }
        
        return chains.get(ineff_type, [
            CausalStep(step_number=1, cause="Inefficiency detected", effect="Operational deviation", confidence=0.7),
        ])
    
    def _categorize_root_cause(self, ineff_type: str) -> str:
        """Categorize the root cause type."""
        categories = {
            "OVERLOAD": "capacity",
            "UNDERUTILIZATION": "capacity",
            "LOAD_IMBALANCE": "capacity",
            "IDLE_TIME": "resource",
            "WAIT_TIME": "process",
            "DELAY": "process",
            "BOTTLENECK": "process",
            "REWORK": "quality",
            "EXCESSIVE_HANDOVERS": "process",
            "BOUNCE": "process",
            "ESCALATION": "complexity",
            "SLA_RISK": "time",
            "SLA_BREACH": "time",
            "BLOCKED": "dependency",
            "OFFLINE": "resource",
        }
        return categories.get(ineff_type, "general")
    
    def _calculate_probability(self, detection: Dict) -> float:
        """Calculate probability of root cause correctness."""
        severity = detection.get("severity_score", 0.5)
        deviation = detection.get("deviation_percent", 10)
        
        base_prob = 0.7
        severity_bonus = severity * 0.15
        deviation_bonus = min(abs(deviation) / 100, 0.1)
        
        return min(base_prob + severity_bonus + deviation_bonus, 0.95)
    
    def _gather_evidence(self, detection: Dict) -> List[str]:
        """Gather evidence for the analysis."""
        evidence = []
        
        ineff_type = detection.get("inefficiency_type") or detection.get("anomaly_type", "")
        location = detection.get("location_id") or detection.get("anomaly_location", "")
        deviation = detection.get("deviation_percent", 0)
        current = detection.get("current_value")
        expected = detection.get("expected_value")
        
        evidence.append(f"Detected {ineff_type} at {location}")
        
        if current is not None and expected is not None:
            evidence.append(f"Current: {current}, Expected: {expected}")
        
        if deviation:
            evidence.append(f"Deviation: {deviation:.1f}%")
        
        return evidence
    
    def _generate_optimization_plan(
        self,
        detections: List[Dict],
        root_causes: List[RootCauseExplanation],
        financial_loss: Optional[Dict]
    ) -> OptimizationPlan:
        """Generate optimization plan - universal actions."""
        plan_id = f"plan-{uuid.uuid4().hex[:8]}"
        
        load_rebalancing = None
        reassignments = None
        priority_changes = None
        capacity_adjustments = None
        process_optimizations = None
        alerts = None
        
        steps = []
        
        for detection in detections:
            ineff_type = detection.get("inefficiency_type") or detection.get("anomaly_type", "")
            location = detection.get("location_id") or detection.get("anomaly_location", "")
            
            # Capacity issues -> rebalance
            if ineff_type in ["OVERLOAD", "UNDERUTILIZATION", "LOAD_IMBALANCE"]:
                load_rebalancing = {
                    "action": "REBALANCE_LOAD",
                    "targets": [location] if load_rebalancing is None else load_rebalancing.get("targets", []) + [location],
                    "reason": f"Address {ineff_type}",
                }
                steps.append(f"Rebalance workload at {location}")
            
            # SLA issues -> prioritize and alert
            if ineff_type in ["SLA_RISK", "SLA_BREACH"]:
                priority_changes = {
                    "action": "PRIORITIZE",
                    "targets": [location],
                    "new_priority": "urgent",
                    "reason": "SLA at risk",
                }
                alerts = {
                    "action": "ALERT_SUPERVISOR",
                    "targets": [location],
                    "urgency": "high" if ineff_type == "SLA_BREACH" else "medium",
                }
                steps.append(f"Prioritize and expedite {location}")
            
            # Flow issues -> reassign or reroute
            if ineff_type in ["EXCESSIVE_HANDOVERS", "BOUNCE", "REWORK"]:
                process_optimizations = {
                    "action": "REROUTE",
                    "targets": [location],
                    "reason": f"Reduce {ineff_type.lower().replace('_', ' ')}",
                }
                steps.append(f"Optimize workflow for {location}")
            
            # Bottleneck -> add capacity
            if ineff_type == "BOTTLENECK":
                capacity_adjustments = {
                    "action": "ADD_CAPACITY",
                    "targets": [location],
                    "reason": "Address bottleneck",
                }
                steps.append(f"Add capacity at bottleneck {location}")
            
            # Idle/blocked -> reassign
            if ineff_type in ["IDLE_TIME", "BLOCKED"]:
                reassignments = {
                    "action": "REASSIGN",
                    "targets": [location],
                    "reason": f"Resource is {ineff_type.lower().replace('_', ' ')}",
                }
                steps.append(f"Reassign work {'to' if ineff_type == 'IDLE_TIME' else 'from'} {location}")
        
        # Calculate impact
        total_loss = financial_loss.get("total_loss", 0) if financial_loss else 0
        estimated_impact = {
            "potential_savings": total_loss * 0.65,
            "efficiency_improvement_percent": 15,
            "implementation_time_hours": 2,
        }
        
        return OptimizationPlan(
            plan_id=plan_id,
            load_rebalancing=load_rebalancing,
            reassignments=reassignments,
            priority_changes=priority_changes,
            capacity_adjustments=capacity_adjustments,
            process_optimizations=process_optimizations,
            alerts_to_send=alerts,
            estimated_impact=estimated_impact,
            implementation_steps=steps if steps else ["Review detected issues and take appropriate action"],
            timestamp=datetime.now(),
        )
    
    def _create_pending_actions(
        self, 
        plan: OptimizationPlan,
        detections: List[Dict]
    ) -> List[ExecutionAction]:
        """Create pending actions for COPILOT mode."""
        actions = []
        
        if plan.load_rebalancing:
            actions.append(ExecutionAction(
                action_id=f"act-{uuid.uuid4().hex[:8]}",
                action_type="REBALANCE_LOAD",
                target_id=", ".join(plan.load_rebalancing.get("targets", [])),
                target_type="entity",
                parameters=plan.load_rebalancing,
                reason="Address load imbalance",
                status=ActionStatus.PENDING,
                requires_approval=True,
            ))
        
        if plan.priority_changes:
            actions.append(ExecutionAction(
                action_id=f"act-{uuid.uuid4().hex[:8]}",
                action_type="PRIORITIZE",
                target_id=", ".join(plan.priority_changes.get("targets", [])),
                target_type="work_item",
                parameters=plan.priority_changes,
                reason="SLA at risk",
                status=ActionStatus.PENDING,
                requires_approval=True,
            ))
        
        return actions
    
    def _execute_actions(
        self, 
        plan: OptimizationPlan,
        detections: List[Dict]
    ) -> List[ExecutionAction]:
        """Execute actions autonomously in FULL_AUTO mode."""
        actions = []
        
        if plan.load_rebalancing:
            result = self.optimizer_agent.execute(
                recommendation_id=plan.plan_id,
                action_type="REBALANCE_WORKLOAD",
                payload=plan.load_rebalancing,
            )
            actions.append(ExecutionAction(
                action_id=f"act-{uuid.uuid4().hex[:8]}",
                action_type="REBALANCE_LOAD",
                target_id=", ".join(plan.load_rebalancing.get("targets", [])),
                target_type="entity",
                parameters=plan.load_rebalancing,
                reason="Address load imbalance",
                status=ActionStatus.COMPLETED if result.get("status") == "success" else ActionStatus.FAILED,
                result=json.dumps(result.get("details", {})) if isinstance(result.get("details"), dict) else str(result.get("details", "")),
                executed_at=datetime.now(),
                completed_at=datetime.now(),
            ))
        
        if plan.priority_changes:
            actions.append(ExecutionAction(
                action_id=f"act-{uuid.uuid4().hex[:8]}",
                action_type="PRIORITIZE",
                target_id=", ".join(plan.priority_changes.get("targets", [])),
                target_type="work_item",
                parameters=plan.priority_changes,
                reason="SLA at risk",
                status=ActionStatus.COMPLETED,
                result="Priority changed to urgent",
                executed_at=datetime.now(),
                completed_at=datetime.now(),
            ))
        
        if plan.alerts_to_send:
            actions.append(ExecutionAction(
                action_id=f"act-{uuid.uuid4().hex[:8]}",
                action_type="ALERT_SUPERVISOR",
                target_id=", ".join(plan.alerts_to_send.get("targets", [])),
                target_type="entity",
                parameters=plan.alerts_to_send,
                reason="SLA issue detected",
                status=ActionStatus.COMPLETED,
                result="Alert sent to supervisor",
                executed_at=datetime.now(),
                completed_at=datetime.now(),
            ))
        
        if plan.process_optimizations:
            actions.append(ExecutionAction(
                action_id=f"act-{uuid.uuid4().hex[:8]}",
                action_type="REROUTE",
                target_id=", ".join(plan.process_optimizations.get("targets", [])),
                target_type="work_item",
                parameters=plan.process_optimizations,
                reason="Optimize workflow",
                status=ActionStatus.COMPLETED,
                result="Workflow routing optimized",
                executed_at=datetime.now(),
                completed_at=datetime.now(),
            ))
        
        return actions
    
    def _learn_from_results(
        self,
        detections: List[Dict],
        actions: List[ExecutionAction]
    ) -> UpdatedBaselines:
        """Learn from results and update baselines."""
        baseline_updates = {}
        threshold_updates = {}
        notes = []
        
        # Track successful actions
        successful = [a for a in actions if a.status == ActionStatus.COMPLETED]
        if successful:
            notes.append(f"Successfully executed {len(successful)} corrective actions")
        
        # Update learning history
        self._learning_history.append({
            "timestamp": datetime.now().isoformat(),
            "industry": self._industry,
            "detections_count": len(detections),
            "actions_count": len(actions),
            "successful_actions": len(successful),
        })
        
        return UpdatedBaselines(
            baseline_updates=baseline_updates,
            threshold_updates=threshold_updates,
            learning_notes=notes,
        )
    
    def _convert_to_detections(self, detections: List[Dict]) -> List[InefficiencyDetection]:
        """Convert detection dicts to InefficiencyDetection models."""
        result = []
        for d in detections:
            try:
                severity = d.get("severity_score", 0.5)
                severity_level = (
                    SeverityLevel.LOW if severity < 0.3
                    else SeverityLevel.MEDIUM if severity < 0.6
                    else SeverityLevel.HIGH if severity < 0.85
                    else SeverityLevel.CRITICAL
                )
                
                result.append(InefficiencyDetection(
                    detection_id=d.get("detection_id", f"det-{uuid.uuid4().hex[:8]}"),
                    inefficiency_type=d.get("inefficiency_type") or d.get("anomaly_type", "UNKNOWN"),
                    location_id=d.get("location_id") or d.get("anomaly_location", "unknown"),
                    location_type=d.get("location_type", "entity"),
                    location_name=d.get("location_name"),
                    severity_score=severity,
                    severity_level=severity_level,
                    time_window=d.get("time_window", {"start": datetime.now(), "end": datetime.now()}),
                    deviation_percent=d.get("deviation_percent", 0),
                    current_value=d.get("current_value"),
                    expected_value=d.get("expected_value"),
                    description=d.get("description", ""),
                    timestamp=datetime.now(),
                ))
            except Exception:
                continue
        return result
    
    def _convert_to_financial_loss(self, loss_data: Dict) -> FinancialLoss:
        """Convert loss dict to FinancialLoss model."""
        breakdown_data = loss_data.get("breakdown", {})
        breakdown = LossBreakdown(
            base_loss=breakdown_data.get("base_loss", 0),
            industry_adjustment=breakdown_data.get("industry_adjustment", 0),
            severity_adjustment=breakdown_data.get("severity_adjustment", 0),
        )
        
        total = loss_data.get("total_loss", 0)
        
        return FinancialLoss(
            total_loss=total,
            currency=loss_data.get("currency", "INR"),
            loss_per_hour=loss_data.get("money_lost_per_min", 0) * 60 if loss_data.get("money_lost_per_min") else total / 8,
            loss_per_day=total,
            projected_24h_loss=loss_data.get("projected_future_loss", total * 1.5),
            projected_weekly_loss=total * 7,
            savings_if_fixed=loss_data.get("savings_if_fixed", total * 0.65),
            breakdown=breakdown,
            by_type=loss_data.get("by_type", {}),
            by_location=loss_data.get("by_source", {}),
            confidence=loss_data.get("confidence", 0.7),
            methodology=loss_data.get("methodology", "Standard calculation"),
            timestamp=datetime.now(),
        )
    
    def get_status(self) -> Dict[str, Any]:
        """Get orchestrator status."""
        return {
            "pipeline_id": self._pipeline_id,
            "mode": self._mode.value,
            "industry": self._industry,
            "agents": {
                "detection": self.detection_agent.get_status(),
                "knowledge_graph": self.knowledge_graph_agent.get_status(),
                "loss_estimation": self.loss_estimation_agent.get_status(),
            },
            "baselines": self._baselines,
            "learning_history_count": len(self._learning_history),
        }
