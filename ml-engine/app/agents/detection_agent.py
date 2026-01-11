"""
AOIA ML Engine - Universal Detection Agent
Detects operational inefficiencies across ANY industry/workflow.

Works for: BPO, SaaS, Retail, Healthcare, Logistics, Agencies, HR, Finance, etc.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

from app.agents.base_agent import BaseAgent
from app.models.output_schemas import InefficiencyDetection, SeverityLevel


class DetectionAgent(BaseAgent):
    """
    Universal Detection Agent - Detects inefficiencies in ANY operational workflow.
    
    NOT limited to machines! Works with:
    - Agents, operators, employees, teams
    - Tickets, tasks, orders, cases, projects
    - Queues, stages, processes
    - Any entity with state, time, and throughput
    
    Inputs: Entities, work items, processes, events
    Outputs: Inefficiency detections with severity scores
    """
    
    def __init__(self):
        super().__init__("detection")
        
        # Universal detection thresholds
        self.thresholds = {
            # Load thresholds
            "overload_percent": 90,          # Above this = overloaded
            "underutilization_percent": 40,  # Below this = underutilized
            "load_imbalance_variance": 20,   # Variance threshold
            
            # Time thresholds
            "idle_time_minutes": 15,         # Idle for this long = issue
            "wait_time_minutes": 30,         # Waiting this long = issue
            
            # Workflow thresholds
            "handover_count": 3,             # More than this = excessive
            "rework_count": 2,               # More than this = quality issue
            "bounce_count": 2,               # More than this = process issue
            "escalation_count": 2,           # More than this = problem
            
            # Queue thresholds
            "queue_size": 10,                # Above this = overflow risk
            
            # SLA thresholds
            "sla_remaining_percent": 20,     # Below this = at risk
            
            # Throughput thresholds
            "throughput_drop_percent": 20,   # Drop by this much = issue
        }
        
        # Baselines (can be updated per industry)
        self.baselines: Dict[str, float] = {}
    
    def process(
        self, 
        input_data: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process operational data to detect inefficiencies.
        
        Works with universal input format:
        - entities: People, machines, systems, stations, teams
        - work_items: Tasks, tickets, orders, cases, projects
        - processes: Workflow definitions
        - events: Operational events
        """
        start_time = self._start_processing()
        detections: List[InefficiencyDetection] = []
        
        try:
            # Extract data (support both new and legacy formats)
            entities = input_data.get("entities", [])
            work_items = input_data.get("work_items", [])
            processes = input_data.get("processes", [])
            business = input_data.get("business", {})
            
            # Legacy format support
            if not entities:
                entities = input_data.get("machines", []) + input_data.get("shifts", [])
            if not work_items:
                work_items = input_data.get("workflows", [])
            
            # Update baselines from business context
            if business:
                self._update_baselines(business)
            
            # Detect entity-level inefficiencies
            for entity in entities:
                entity_detections = self._detect_entity_issues(entity)
                detections.extend(entity_detections)
            
            # Detect work item inefficiencies
            for item in work_items:
                item_detections = self._detect_work_item_issues(item)
                detections.extend(item_detections)
            
            # Detect process-level inefficiencies
            for process in processes:
                process_detections = self._detect_process_issues(process)
                detections.extend(process_detections)
            
            # Detect cross-entity patterns (load imbalance)
            if len(entities) > 1:
                pattern_detections = self._detect_patterns(entities, work_items)
                detections.extend(pattern_detections)
            
            self._complete_processing(start_time, success=True)
            self._last_output = {"detections": [d.model_dump() for d in detections]}
            
            return {
                "status": "success",
                "detections": [d.model_dump() for d in detections],
                "count": len(detections),
                "processing_time_ms": (datetime.now() - start_time).total_seconds() * 1000,
            }
            
        except Exception as e:
            self._log_error(e, "Detection processing failed")
            self._complete_processing(start_time, success=False)
            return {"status": "error", "error": str(e), "detections": []}
    
    def _update_baselines(self, business: Dict[str, Any]) -> None:
        """Update baselines from business context."""
        if business.get("baseline_throughput"):
            self.baselines["throughput"] = business["baseline_throughput"]
        if business.get("baseline_items_per_hour"):
            self.baselines["items_per_hour"] = business["baseline_items_per_hour"]
        if business.get("baseline_resolution_time_minutes"):
            self.baselines["resolution_time"] = business["baseline_resolution_time_minutes"]
        # Legacy support
        if business.get("baseline_output_per_min"):
            self.baselines["throughput"] = business["baseline_output_per_min"] * 60
    
    def _detect_entity_issues(self, entity: Dict[str, Any]) -> List[InefficiencyDetection]:
        """Detect issues with any operational entity (person, system, station, etc.)."""
        detections = []
        
        entity_id = entity.get("entity_id") or entity.get("machine_id") or entity.get("operator_id") or "unknown"
        entity_type = entity.get("entity_type", "entity")
        entity_name = entity.get("entity_name", entity_id)
        state = entity.get("state") or entity.get("machine_state", "active")
        
        # ========== IDLE TIME ==========
        idle_time = entity.get("idle_time_minutes", 0)
        if idle_time >= self.thresholds["idle_time_minutes"]:
            severity = min(idle_time / 60, 1.0)  # Scale up to 1 hour
            detections.append(self._create_detection(
                inefficiency_type="IDLE_TIME",
                location_id=entity_id,
                location_type=entity_type,
                location_name=entity_name,
                severity=severity,
                deviation=idle_time,
                current_value=idle_time,
                expected_value=0,
                description=f"{entity_name} has been idle for {idle_time:.0f} minutes"
            ))
        
        # ========== STATE-BASED (idle, blocked, offline) ==========
        if state in ["idle", "blocked", "offline", "down"]:
            severity_map = {"idle": 0.4, "blocked": 0.7, "offline": 0.8, "down": 0.9}
            severity = severity_map.get(state, 0.5)
            inefficiency_type = "BLOCKED" if state == "blocked" else ("OFFLINE" if state in ["offline", "down"] else "IDLE_TIME")
            detections.append(self._create_detection(
                inefficiency_type=inefficiency_type,
                location_id=entity_id,
                location_type=entity_type,
                location_name=entity_name,
                severity=severity,
                deviation=100,
                description=f"{entity_name} is in '{state}' state"
            ))
        
        # ========== OVERLOAD ==========
        load = entity.get("load_percent") or entity.get("operator_load", 0)
        if load >= self.thresholds["overload_percent"]:
            severity = min((load - 80) / 20, 1.0)  # Scale 80-100 to 0-1
            detections.append(self._create_detection(
                inefficiency_type="OVERLOAD",
                location_id=entity_id,
                location_type=entity_type,
                location_name=entity_name,
                severity=severity,
                deviation=load - 80,
                current_value=load,
                expected_value=80,
                description=f"{entity_name} is at {load}% load - risk of burnout/errors/delays"
            ))
        
        # ========== UNDERUTILIZATION ==========
        elif load > 0 and load < self.thresholds["underutilization_percent"]:
            severity = (self.thresholds["underutilization_percent"] - load) / 40
            detections.append(self._create_detection(
                inefficiency_type="UNDERUTILIZATION",
                location_id=entity_id,
                location_type=entity_type,
                location_name=entity_name,
                severity=min(severity, 0.7),
                deviation=self.thresholds["underutilization_percent"] - load,
                current_value=load,
                expected_value=self.thresholds["underutilization_percent"],
                description=f"{entity_name} is only at {load}% load - underutilized"
            ))
        
        # ========== QUEUE OVERFLOW ==========
        queue_size = entity.get("queue_size", 0)
        if queue_size >= self.thresholds["queue_size"]:
            severity = min(queue_size / 20, 1.0)
            detections.append(self._create_detection(
                inefficiency_type="QUEUE_OVERFLOW",
                location_id=entity_id,
                location_type=entity_type,
                location_name=entity_name,
                severity=severity,
                deviation=queue_size - self.thresholds["queue_size"],
                current_value=queue_size,
                expected_value=self.thresholds["queue_size"],
                description=f"{entity_name} has {queue_size} items in queue - overflow risk"
            ))
        
        # ========== LOW THROUGHPUT ==========
        throughput = entity.get("throughput") or entity.get("output_per_min", 0)
        baseline = self.baselines.get("throughput", 0)
        if throughput and baseline and throughput < baseline * (1 - self.thresholds["throughput_drop_percent"] / 100):
            deviation = (baseline - throughput) / baseline * 100
            severity = min(deviation / 50, 1.0)
            detections.append(self._create_detection(
                inefficiency_type="LOW_THROUGHPUT",
                location_id=entity_id,
                location_type=entity_type,
                location_name=entity_name,
                severity=severity,
                deviation=deviation,
                current_value=throughput,
                expected_value=baseline,
                description=f"{entity_name} throughput is {deviation:.1f}% below baseline"
            ))
        
        return detections
    
    def _detect_work_item_issues(self, item: Dict[str, Any]) -> List[InefficiencyDetection]:
        """Detect issues with work items (tickets, tasks, orders, cases, etc.)."""
        detections = []
        
        item_id = item.get("item_id") or item.get("task_id") or "unknown"
        item_type = item.get("item_type", "work_item")
        item_name = item.get("item_name", item_id)
        
        # ========== EXCESSIVE HANDOVERS ==========
        handovers = item.get("handover_count") or item.get("task_transfers", 0)
        if handovers >= self.thresholds["handover_count"]:
            severity = min(handovers / 8, 1.0)
            detections.append(self._create_detection(
                inefficiency_type="EXCESSIVE_HANDOVERS",
                location_id=item_id,
                location_type=item_type,
                location_name=item_name,
                severity=severity,
                deviation=handovers * 15,
                current_value=handovers,
                expected_value=self.thresholds["handover_count"],
                description=f"{item_type.title()} {item_id} has {handovers} handovers - workflow inefficiency"
            ))
        
        # ========== REWORK ==========
        rework = item.get("rework_count") or item.get("rework_loops", 0)
        if rework >= self.thresholds["rework_count"]:
            severity = min(rework / 5, 1.0)
            detections.append(self._create_detection(
                inefficiency_type="REWORK",
                location_id=item_id,
                location_type=item_type,
                location_name=item_name,
                severity=severity,
                deviation=rework * 25,
                current_value=rework,
                expected_value=0,
                description=f"{item_type.title()} {item_id} has been reworked {rework} times - quality issue"
            ))
        
        # ========== BOUNCE BACK ==========
        bounces = item.get("bounce_count", 0)
        if bounces >= self.thresholds["bounce_count"]:
            severity = min(bounces / 5, 1.0)
            detections.append(self._create_detection(
                inefficiency_type="BOUNCE",
                location_id=item_id,
                location_type=item_type,
                location_name=item_name,
                severity=severity,
                deviation=bounces * 20,
                current_value=bounces,
                expected_value=0,
                description=f"{item_type.title()} {item_id} bounced back {bounces} times - process issue"
            ))
        
        # ========== ESCALATIONS ==========
        escalations = item.get("escalation_count", 0)
        if escalations >= self.thresholds["escalation_count"]:
            severity = min(escalations / 4, 1.0)
            detections.append(self._create_detection(
                inefficiency_type="ESCALATION",
                location_id=item_id,
                location_type=item_type,
                location_name=item_name,
                severity=severity,
                deviation=escalations * 20,
                current_value=escalations,
                expected_value=0,
                description=f"{item_type.title()} {item_id} escalated {escalations} times"
            ))
        
        # ========== WAIT TIME ==========
        wait_time = item.get("wait_time_minutes", 0)
        if wait_time >= self.thresholds["wait_time_minutes"]:
            severity = min(wait_time / 120, 1.0)
            detections.append(self._create_detection(
                inefficiency_type="WAIT_TIME",
                location_id=item_id,
                location_type=item_type,
                location_name=item_name,
                severity=severity,
                deviation=wait_time,
                current_value=wait_time,
                expected_value=0,
                description=f"{item_type.title()} {item_id} has been waiting for {wait_time:.0f} minutes"
            ))
        
        # ========== SLA RISK ==========
        sla_remaining = item.get("sla_remaining_minutes")
        sla_target = item.get("sla_target_minutes")
        if sla_remaining is not None and sla_target:
            pct_remaining = (sla_remaining / sla_target) * 100
            if pct_remaining <= 0:
                detections.append(self._create_detection(
                    inefficiency_type="SLA_BREACH",
                    location_id=item_id,
                    location_type=item_type,
                    location_name=item_name,
                    severity=1.0,
                    deviation=abs(sla_remaining),
                    current_value=sla_remaining,
                    expected_value=0,
                    description=f"{item_type.title()} {item_id} has BREACHED SLA by {abs(sla_remaining):.0f} minutes"
                ))
            elif pct_remaining <= self.thresholds["sla_remaining_percent"]:
                severity = (self.thresholds["sla_remaining_percent"] - pct_remaining) / self.thresholds["sla_remaining_percent"]
                detections.append(self._create_detection(
                    inefficiency_type="SLA_RISK",
                    location_id=item_id,
                    location_type=item_type,
                    location_name=item_name,
                    severity=min(severity + 0.5, 1.0),
                    deviation=self.thresholds["sla_remaining_percent"] - pct_remaining,
                    current_value=sla_remaining,
                    expected_value=sla_target,
                    description=f"{item_type.title()} {item_id} at SLA risk - only {sla_remaining:.0f}min remaining"
                ))
        
        # ========== BLOCKED STATUS ==========
        status = item.get("status", "")
        if status in ["blocked", "stuck", "on_hold"]:
            detections.append(self._create_detection(
                inefficiency_type="BLOCKED",
                location_id=item_id,
                location_type=item_type,
                location_name=item_name,
                severity=0.7,
                deviation=100,
                description=f"{item_type.title()} {item_id} is {status}"
            ))
        
        return detections
    
    def _detect_process_issues(self, process: Dict[str, Any]) -> List[InefficiencyDetection]:
        """Detect issues at the process/workflow level."""
        detections = []
        
        process_id = process.get("process_id", "unknown")
        process_name = process.get("process_name", process_id)
        
        # ========== BOTTLENECK STAGE ==========
        bottleneck = process.get("bottleneck_stage")
        if bottleneck:
            detections.append(self._create_detection(
                inefficiency_type="BOTTLENECK",
                location_id=process_id,
                location_type="process",
                location_name=process_name,
                severity=0.7,
                deviation=30,
                description=f"Process '{process_name}' has bottleneck at stage: {bottleneck}"
            ))
        
        return detections
    
    def _detect_patterns(
        self, 
        entities: List[Dict], 
        work_items: List[Dict]
    ) -> List[InefficiencyDetection]:
        """Detect patterns across multiple entities (load imbalance, etc.)."""
        detections = []
        
        # ========== LOAD IMBALANCE ==========
        loads = [e.get("load_percent") or e.get("operator_load", 50) for e in entities if e.get("load_percent") or e.get("operator_load")]
        if len(loads) >= 2:
            avg_load = sum(loads) / len(loads)
            max_load = max(loads)
            min_load = min(loads)
            variance = max_load - min_load
            
            if variance >= self.thresholds["load_imbalance_variance"]:
                severity = min(variance / 50, 1.0)
                detections.append(self._create_detection(
                    inefficiency_type="LOAD_IMBALANCE",
                    location_id="all_entities",
                    location_type="system",
                    location_name="Workload Distribution",
                    severity=severity,
                    deviation=variance,
                    current_value=variance,
                    expected_value=10,
                    description=f"Load imbalance detected: {variance:.0f}% difference (max:{max_load}%, min:{min_load}%)"
                ))
        
        return detections
    
    def _create_detection(
        self,
        inefficiency_type: str,
        location_id: str,
        location_type: str,
        location_name: str,
        severity: float,
        deviation: float,
        description: str,
        current_value: Optional[float] = None,
        expected_value: Optional[float] = None,
    ) -> InefficiencyDetection:
        """Create a standardized detection object."""
        severity = min(max(severity, 0), 1)  # Clamp to 0-1
        severity_level = (
            SeverityLevel.LOW if severity < 0.3
            else SeverityLevel.MEDIUM if severity < 0.6
            else SeverityLevel.HIGH if severity < 0.85
            else SeverityLevel.CRITICAL
        )
        
        return InefficiencyDetection(
            detection_id=f"det-{uuid.uuid4().hex[:12]}",
            inefficiency_type=inefficiency_type,
            location_id=location_id,
            location_type=location_type,
            location_name=location_name,
            severity_score=severity,
            severity_level=severity_level,
            time_window={"start": datetime.now(), "end": datetime.now()},
            deviation_percent=deviation,
            current_value=current_value,
            expected_value=expected_value,
            description=description,
            timestamp=datetime.now(),
        )
    
    def update_thresholds(self, new_thresholds: Dict[str, float]) -> None:
        """Update detection thresholds (for learning/customization)."""
        self.thresholds.update(new_thresholds)
    
    def update_baselines(self, new_baselines: Dict[str, float]) -> None:
        """Update baseline values (for learning)."""
        self.baselines.update(new_baselines)
