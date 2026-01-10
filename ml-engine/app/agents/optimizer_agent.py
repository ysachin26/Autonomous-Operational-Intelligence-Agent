"""
AOIA ML Engine - Optimizer Agent
Generates and executes optimization recommendations.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import random


class OptimizerAgent:
    """
    The AOIA Optimizer Agent analyzes operational data and generates
    actionable recommendations for improving efficiency and reducing losses.
    """
    
    def __init__(self):
        # Optimization strategies by anomaly type
        self.strategies = {
            "IDLE_SPIKE": [
                {
                    "action_type": "REBALANCE_WORKLOAD",
                    "title_template": "Rebalance Workload for {source}",
                    "description_template": "Redistribute tasks to reduce idle time by optimizing queue management",
                    "base_impact": 0.25,
                    "confidence": 0.85,
                },
                {
                    "action_type": "ADJUST_ROUTING",
                    "title_template": "Optimize Task Routing",
                    "description_template": "Modify routing logic to minimize wait times and idle periods",
                    "base_impact": 0.20,
                    "confidence": 0.80,
                },
            ],
            "THROUGHPUT_DROP": [
                {
                    "action_type": "SCHEDULE_MAINTENANCE",
                    "title_template": "Schedule Preventive Maintenance - {source}",
                    "description_template": "Proactive maintenance to restore optimal performance levels",
                    "base_impact": 0.40,
                    "confidence": 0.88,
                },
                {
                    "action_type": "RESOURCE_ALLOCATION",
                    "title_template": "Allocate Additional Resources",
                    "description_template": "Add temporary capacity to meet throughput requirements",
                    "base_impact": 0.35,
                    "confidence": 0.82,
                },
            ],
            "MACHINE_SLOWDOWN": [
                {
                    "action_type": "SCHEDULE_MAINTENANCE",
                    "title_template": "Urgent Maintenance Required - {source}",
                    "description_template": "Machine showing degradation patterns indicating maintenance need",
                    "base_impact": 0.50,
                    "confidence": 0.92,
                },
            ],
            "QUALITY_DECLINE": [
                {
                    "action_type": "MODIFY_PROCESS",
                    "title_template": "Process Parameter Adjustment",
                    "description_template": "Recalibrate process parameters to restore quality standards",
                    "base_impact": 0.45,
                    "confidence": 0.85,
                },
                {
                    "action_type": "TRAINING_NEEDED",
                    "title_template": "Quality Awareness Training",
                    "description_template": "Conduct refresher training on quality standards and procedures",
                    "base_impact": 0.30,
                    "confidence": 0.75,
                },
            ],
            "OVERLOAD": [
                {
                    "action_type": "REBALANCE_WORKLOAD",
                    "title_template": "Emergency Workload Redistribution",
                    "description_template": "Immediately redistribute tasks from overloaded resources",
                    "base_impact": 0.35,
                    "confidence": 0.88,
                },
                {
                    "action_type": "RESOURCE_ALLOCATION",
                    "title_template": "Temporary Resource Surge",
                    "description_template": "Deploy additional resources to handle demand spike",
                    "base_impact": 0.40,
                    "confidence": 0.85,
                },
            ],
            "UNDERPERFORMANCE": [
                {
                    "action_type": "TRAINING_NEEDED",
                    "title_template": "Performance Improvement Training - {source}",
                    "description_template": "Targeted training to address identified skill gaps",
                    "base_impact": 0.35,
                    "confidence": 0.78,
                },
                {
                    "action_type": "ALERT_SUPERVISOR",
                    "title_template": "Supervisor Review Required",
                    "description_template": "Escalate for management review and intervention",
                    "base_impact": 0.20,
                    "confidence": 0.70,
                },
            ],
        }
        
        # Priority mapping
        self.priority_map = {
            "CRITICAL": "URGENT",
            "HIGH": "HIGH",
            "MEDIUM": "MEDIUM",
            "LOW": "LOW",
        }
    
    def generate_recommendations(
        self,
        anomalies: List[Dict[str, Any]],
        incidents: List[Dict[str, Any]],
        current_state: Dict[str, Any],
        constraints: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate optimization recommendations based on current anomalies and state.
        
        Args:
            anomalies: List of detected anomalies
            incidents: List of active incidents
            current_state: Current operational state
            constraints: Business constraints (budget, resources, etc.)
        
        Returns:
            List of recommendations with estimated impact
        """
        recommendations = []
        total_potential_savings = 0
        
        # Process anomalies
        for anomaly in anomalies:
            anomaly_type = anomaly.get("anomalyType", anomaly.get("anomaly_type", "UNKNOWN"))
            source = anomaly.get("source", "unknown")
            severity = anomaly.get("severity", "MEDIUM")
            deviation = abs(anomaly.get("deviation", anomaly.get("deviation_percent", 10)))
            
            # Get applicable strategies
            strategies = self.strategies.get(anomaly_type, [])
            
            for strategy in strategies:
                # Calculate estimated impact
                base_loss = anomaly.get("estimated_loss", deviation * 10 * 75)  # Fallback calculation
                impact = base_loss * strategy["base_impact"]
                
                # Adjust confidence based on severity
                confidence = strategy["confidence"]
                if severity == "CRITICAL":
                    confidence = min(0.98, confidence + 0.05)
                elif severity == "LOW":
                    confidence = max(0.5, confidence - 0.1)
                
                recommendation = {
                    "title": strategy["title_template"].format(source=source),
                    "description": strategy["description_template"],
                    "action_type": strategy["action_type"],
                    "priority": self.priority_map.get(severity, "MEDIUM"),
                    "estimated_impact": round(impact, 2),
                    "confidence": round(confidence, 2),
                    "reasoning": self._generate_reasoning(anomaly_type, source, deviation, strategy),
                    "action_payload": {
                        "source": source,
                        "anomaly_type": anomaly_type,
                        "parameters": self._get_action_parameters(strategy["action_type"], anomaly),
                    },
                }
                
                recommendations.append(recommendation)
                total_potential_savings += impact
        
        # Sort by priority and impact
        priority_order = {"URGENT": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        recommendations.sort(
            key=lambda x: (priority_order.get(x["priority"], 2), -x["estimated_impact"])
        )
        
        # Calculate optimization score
        optimization_score = self._calculate_optimization_score(
            anomalies, recommendations, current_state
        )
        
        return {
            "recommendations": recommendations[:10],  # Top 10 recommendations
            "total_potential_savings": round(total_potential_savings, 2),
            "optimization_score": optimization_score,
        }
    
    def execute(
        self,
        recommendation_id: str,
        action_type: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Execute an approved recommendation.
        
        In production, this would trigger actual system actions.
        For demo, simulates successful execution.
        """
        # Simulate execution
        success_rate = {
            "REBALANCE_WORKLOAD": 0.92,
            "SCHEDULE_MAINTENANCE": 0.95,
            "ADJUST_ROUTING": 0.88,
            "TRAINING_NEEDED": 0.85,
            "RESOURCE_ALLOCATION": 0.90,
            "ALERT_SUPERVISOR": 0.98,
            "MODIFY_PROCESS": 0.82,
        }
        
        rate = success_rate.get(action_type, 0.85)
        success = random.random() < rate
        
        if success:
            # Simulate actual impact (80-120% of estimated)
            impact_multiplier = 0.8 + random.random() * 0.4
            actual_impact = (payload or {}).get("estimated_impact", 10000) * impact_multiplier
            
            return {
                "success": True,
                "message": f"Successfully executed {action_type.replace('_', ' ').lower()} action",
                "actual_impact": round(actual_impact, 2),
                "details": {
                    "action_type": action_type,
                    "execution_time": datetime.now().isoformat(),
                    "affected_resources": [payload.get("source", "unknown")] if payload else [],
                },
            }
        else:
            return {
                "success": False,
                "message": f"Failed to execute {action_type.replace('_', ' ').lower()} action. Manual intervention required.",
                "details": {
                    "action_type": action_type,
                    "error": "Execution failed - resource unavailable or constraint violation",
                },
            }
    
    def simulate(
        self,
        action_type: str,
        target: str,
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Simulate the effect of an optimization before executing.
        """
        # Base impact estimates by action type
        base_impacts = {
            "REBALANCE_WORKLOAD": 25000,
            "SCHEDULE_MAINTENANCE": 45000,
            "ADJUST_ROUTING": 18000,
            "TRAINING_NEEDED": 15000,
            "RESOURCE_ALLOCATION": 35000,
            "ALERT_SUPERVISOR": 8000,
            "MODIFY_PROCESS": 22000,
        }
        
        base_impact = base_impacts.get(action_type, 20000)
        
        # Adjust based on parameters
        severity_mult = parameters.get("severity_multiplier", 1.0)
        simulated_impact = base_impact * severity_mult
        
        # Assess risks
        risks = self._assess_risks(action_type, target, parameters)
        
        # Calculate confidence
        confidence = 0.85 - (len(risks) * 0.05)
        
        return {
            "impact": round(simulated_impact, 2),
            "risks": risks,
            "confidence": round(max(0.5, confidence), 2),
            "recommendation": "PROCEED" if confidence > 0.7 and len(risks) < 3 else "REVIEW",
        }
    
    def _generate_reasoning(
        self,
        anomaly_type: str,
        source: str,
        deviation: float,
        strategy: Dict,
    ) -> str:
        """Generate human-readable reasoning for a recommendation."""
        
        reasoning_templates = {
            "REBALANCE_WORKLOAD": f"Analysis shows {source} has uneven workload distribution. Rebalancing could reduce inefficiency by {strategy['base_impact']*100:.0f}% based on similar past optimizations.",
            "SCHEDULE_MAINTENANCE": f"Predictive analysis indicates {source} is showing early signs of degradation. Preventive maintenance now can avoid {strategy['base_impact']*100:.0f}% of potential downtime costs.",
            "ADJUST_ROUTING": f"Current routing logic causes delays at {source}. Optimization would improve flow efficiency by approximately {strategy['base_impact']*100:.0f}%.",
            "TRAINING_NEEDED": f"Performance patterns on {source} suggest skill gaps. Targeted training typically yields {strategy['base_impact']*100:.0f}% improvement.",
            "RESOURCE_ALLOCATION": f"Demand analysis shows {source} needs additional capacity. Temporary allocation can capture {strategy['base_impact']*100:.0f}% of lost opportunity.",
            "ALERT_SUPERVISOR": f"Situation at {source} requires human judgment. Supervisor intervention addresses {strategy['base_impact']*100:.0f}% of similar cases.",
            "MODIFY_PROCESS": f"Process parameters at {source} have drifted {deviation:.1f}% from optimal. Adjustment can recover {strategy['base_impact']*100:.0f}% efficiency.",
        }
        
        return reasoning_templates.get(
            strategy["action_type"],
            f"Based on {deviation:.1f}% deviation detected at {source}, this action can recover approximately {strategy['base_impact']*100:.0f}% of the impact."
        )
    
    def _get_action_parameters(
        self,
        action_type: str,
        anomaly: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Get specific parameters for an action type."""
        
        params = {
            "anomaly_id": anomaly.get("id"),
            "source": anomaly.get("source"),
            "severity": anomaly.get("severity"),
            "deviation": anomaly.get("deviation", anomaly.get("deviation_percent")),
        }
        
        # Add action-specific parameters
        if action_type == "SCHEDULE_MAINTENANCE":
            params["maintenance_type"] = "preventive"
            params["urgency"] = "within_24h" if anomaly.get("severity") == "CRITICAL" else "within_week"
        elif action_type == "REBALANCE_WORKLOAD":
            params["rebalance_target"] = 0.85  # Target utilization
        elif action_type == "ADJUST_ROUTING":
            params["optimization_goal"] = "minimize_wait_time"
        
        return params
    
    def _calculate_optimization_score(
        self,
        anomalies: List[Dict],
        recommendations: List[Dict],
        current_state: Dict,
    ) -> float:
        """Calculate an overall optimization score (0-100)."""
        
        base_score = 100
        
        # Deduct for anomalies
        anomaly_penalty = len(anomalies) * 3
        base_score -= min(30, anomaly_penalty)
        
        # Bonus for having recommendations
        if recommendations:
            base_score += min(10, len(recommendations) * 2)
        
        # Consider current efficiency if available
        current_efficiency = current_state.get("efficiency", 85)
        base_score = (base_score + current_efficiency) / 2
        
        return round(max(0, min(100, base_score)), 1)
    
    def _assess_risks(
        self,
        action_type: str,
        target: str,
        parameters: Dict,
    ) -> List[str]:
        """Assess risks associated with an optimization action."""
        
        risks = []
        
        risk_factors = {
            "SCHEDULE_MAINTENANCE": [
                "Temporary production interruption during maintenance",
                "Spare parts availability uncertainty",
            ],
            "REBALANCE_WORKLOAD": [
                "Temporary efficiency dip during transition",
                "Potential operator adjustment period",
            ],
            "RESOURCE_ALLOCATION": [
                "Additional cost for temporary resources",
                "Training time for new resources",
            ],
            "MODIFY_PROCESS": [
                "Quality verification needed post-change",
                "Rollback plan required",
            ],
        }
        
        action_risks = risk_factors.get(action_type, [])
        
        # Add generic risks based on parameters
        severity = parameters.get("severity_multiplier", 1.0)
        if severity > 1.5:
            risks.append("High severity requires careful monitoring")
        
        risks.extend(action_risks[:2])  # Limit to 2 specific risks
        
        return risks
