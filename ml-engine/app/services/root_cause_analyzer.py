"""
AOIA ML Engine - Root Cause Analyzer Service
AI-powered root cause analysis for operational anomalies.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import random


class RootCauseAnalyzer:
    """
    Performs root cause analysis using pattern matching and AI reasoning.
    In production, this would integrate with an LLM for deeper analysis.
    """
    
    def __init__(self):
        # Knowledge base of common root causes
        self.cause_patterns = {
            "IDLE_SPIKE": [
                ("Workflow bottleneck at upstream station", 0.35),
                ("Material shortage or delayed delivery", 0.25),
                ("Staffing gap during shift transition", 0.20),
                ("Equipment setup or changeover time", 0.15),
                ("Communication delay in task assignment", 0.05),
            ],
            "THROUGHPUT_DROP": [
                ("Machine performance degradation", 0.30),
                ("Quality issues requiring rework", 0.25),
                ("Operator skill gap or training needed", 0.20),
                ("Supply chain disruption", 0.15),
                ("Process parameter drift", 0.10),
            ],
            "MACHINE_SLOWDOWN": [
                ("Mechanical wear requiring maintenance", 0.35),
                ("Calibration drift", 0.25),
                ("Thermal management issues", 0.20),
                ("Software/firmware issue", 0.10),
                ("Power supply fluctuation", 0.10),
            ],
            "QUALITY_DECLINE": [
                ("Sensor calibration required", 0.30),
                ("Raw material quality variation", 0.25),
                ("Process parameter out of spec", 0.20),
                ("Environmental conditions change", 0.15),
                ("Operator error or inconsistency", 0.10),
            ],
            "OVERLOAD": [
                ("Demand spike exceeding capacity", 0.35),
                ("Resource allocation imbalance", 0.25),
                ("Unexpected task complexity", 0.20),
                ("Staffing shortage", 0.15),
                ("Sequential bottleneck cascade", 0.05),
            ],
            "RESPONSE_DELAY": [
                ("System performance degradation", 0.30),
                ("Network latency issues", 0.25),
                ("Database query optimization needed", 0.20),
                ("Integration point failure", 0.15),
                ("Queue backlog accumulation", 0.10),
            ],
            "UNDERPERFORMANCE": [
                ("Training or skill gap", 0.35),
                ("Unclear work instructions", 0.25),
                ("Tool or equipment issues", 0.20),
                ("Motivation or engagement factors", 0.15),
                ("External distractions", 0.05),
            ],
        }
        
        # Contributing factor templates
        self.contributing_factors = {
            "MANUFACTURING": [
                "Production schedule pressure",
                "Preventive maintenance overdue",
                "Environmental conditions (temperature/humidity)",
                "Shift handover gaps",
            ],
            "BPO": [
                "Call volume spike",
                "System response time",
                "Agent scheduling gaps",
                "Complex query handling",
            ],
        }
    
    def analyze(
        self,
        anomaly_type: str,
        source: str,
        value: float,
        expected_value: float,
        timestamp: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Perform root cause analysis for an anomaly.
        
        Args:
            anomaly_type: Type of the anomaly
            source: Source of the anomaly
            value: Actual observed value
            expected_value: Expected/baseline value
            timestamp: When the anomaly occurred
            context: Additional context data
        
        Returns:
            Root cause analysis result
        """
        # Get potential causes for this anomaly type
        causes = self.cause_patterns.get(anomaly_type, [
            ("Unknown pattern - requires investigation", 0.5),
            ("External factor", 0.3),
            ("Data collection error", 0.2),
        ])
        
        # Select primary cause (in production, this would use ML/LLM)
        primary_cause, confidence = self._select_primary_cause(
            causes, source, value, expected_value, context
        )
        
        # Generate contributing factors
        industry = context.get("industry", "MANUFACTURING") if context else "MANUFACTURING"
        contributing = self._get_contributing_factors(anomaly_type, industry, context)
        
        # Generate evidence points
        evidence = self._generate_evidence(
            anomaly_type, source, value, expected_value, timestamp
        )
        
        # Generate recommended actions
        actions = self._generate_actions(anomaly_type, primary_cause, confidence)
        
        return {
            "primary_cause": primary_cause,
            "confidence": confidence,
            "contributing_factors": contributing,
            "evidence": evidence,
            "recommended_actions": actions,
        }
    
    def _select_primary_cause(
        self,
        causes: List[tuple],
        source: str,
        value: float,
        expected_value: float,
        context: Optional[Dict[str, Any]],
    ) -> tuple:
        """Select the most likely primary cause."""
        # In a real system, this would use ML models or LLM reasoning
        # For demo, use weighted random selection with adjustments
        
        deviation = abs(value - expected_value) / expected_value if expected_value else 0
        
        # Adjust probabilities based on deviation severity
        adjusted_causes = []
        for cause, base_prob in causes:
            # Higher deviations slightly favor mechanical/severe causes
            if deviation > 0.3 and "maintenance" in cause.lower():
                adjusted_prob = min(0.95, base_prob * 1.3)
            elif deviation > 0.3 and "degradation" in cause.lower():
                adjusted_prob = min(0.95, base_prob * 1.2)
            else:
                adjusted_prob = base_prob
            adjusted_causes.append((cause, adjusted_prob))
        
        # Select based on adjusted probability
        # For demo consistency, use deterministic selection
        sorted_causes = sorted(adjusted_causes, key=lambda x: -x[1])
        primary_cause = sorted_causes[0][0]
        confidence = round(sorted_causes[0][1] + random.uniform(0.05, 0.15), 2)
        
        return primary_cause, min(0.95, confidence)
    
    def _get_contributing_factors(
        self,
        anomaly_type: str,
        industry: str,
        context: Optional[Dict[str, Any]],
    ) -> List[str]:
        """Get relevant contributing factors."""
        base_factors = self.contributing_factors.get(industry, [])
        
        # Add anomaly-specific factors
        specific_factors = {
            "IDLE_SPIKE": ["Task queue management", "Resource availability"],
            "THROUGHPUT_DROP": ["Maintenance schedule adherence", "Input quality"],
            "MACHINE_SLOWDOWN": ["Operating temperature", "Component wear"],
            "QUALITY_DECLINE": ["Inspection frequency", "Calibration schedule"],
            "OVERLOAD": ["Capacity planning accuracy", "Demand forecasting"],
        }
        
        factors = list(base_factors)
        if anomaly_type in specific_factors:
            factors.extend(specific_factors[anomaly_type])
        
        return factors[:4]  # Return top 4 factors
    
    def _generate_evidence(
        self,
        anomaly_type: str,
        source: str,
        value: float,
        expected_value: float,
        timestamp: str,
    ) -> List[str]:
        """Generate evidence points supporting the analysis."""
        deviation = ((value - expected_value) / expected_value * 100) if expected_value else 0
        
        evidence = [
            f"Metric value ({value:.1f}) deviated {abs(deviation):.1f}% from expected ({expected_value:.1f})",
            f"Anomaly detected on source: {source}",
            f"Event timestamp: {timestamp}",
        ]
        
        # Add contextual evidence
        if abs(deviation) > 30:
            evidence.append("Significant deviation indicates potential systemic issue")
        
        if "machine" in source.lower():
            evidence.append("Machine-related source suggests equipment investigation")
        elif "shift" in source.lower():
            evidence.append("Shift-related source suggests workforce or scheduling review")
        
        return evidence
    
    def _generate_actions(
        self,
        anomaly_type: str,
        primary_cause: str,
        confidence: float,
    ) -> List[str]:
        """Generate recommended actions based on the analysis."""
        actions = []
        
        # High-priority action based on anomaly type
        priority_actions = {
            "IDLE_SPIKE": "Review workflow and task distribution for bottlenecks",
            "THROUGHPUT_DROP": "Conduct equipment inspection and performance check",
            "MACHINE_SLOWDOWN": "Schedule preventive maintenance inspection",
            "QUALITY_DECLINE": "Verify sensor calibration and inspection parameters",
            "OVERLOAD": "Assess resource allocation and consider load balancing",
            "RESPONSE_DELAY": "Monitor system performance and check infrastructure",
            "UNDERPERFORMANCE": "Review operator training needs and work conditions",
        }
        
        if anomaly_type in priority_actions:
            actions.append(priority_actions[anomaly_type])
        
        # Add cause-specific actions
        if "maintenance" in primary_cause.lower():
            actions.append("Schedule immediate maintenance review")
        if "training" in primary_cause.lower() or "skill" in primary_cause.lower():
            actions.append("Arrange targeted training session")
        if "calibration" in primary_cause.lower():
            actions.append("Perform device calibration check")
        
        # Add monitoring action
        actions.append("Set up enhanced monitoring for next 24 hours")
        
        # Add escalation if high confidence
        if confidence > 0.8:
            actions.append("Escalate to supervisor for immediate attention")
        
        return actions[:5]  # Return top 5 actions
