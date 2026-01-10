"""
AOIA ML Engine - Loss Calculator Service
Quantifies operational inefficiencies in monetary terms.
"""

from typing import Dict, Any


class LossCalculator:
    """
    Calculates monetary loss from operational inefficiencies.
    
    Core Formula:
    loss = (expected_output - actual_output) × cost_per_minute × duration
    
    Adjusted by industry-specific multipliers and anomaly type weights.
    """
    
    def __init__(self):
        # Industry-specific cost multipliers
        self.industry_multipliers = {
            "MANUFACTURING": 1.2,
            "BPO": 0.8,
            "LOGISTICS": 1.1,
            "RETAIL": 0.9,
            "HEALTHCARE": 1.5,
            "GENERAL": 1.0,
        }
        
        # Anomaly type impact weights
        self.anomaly_weights = {
            "IDLE_SPIKE": 0.8,
            "THROUGHPUT_DROP": 1.2,
            "RESPONSE_DELAY": 0.7,
            "MACHINE_SLOWDOWN": 1.3,
            "QUALITY_DECLINE": 1.5,  # Quality issues have cascading costs
            "OVERLOAD": 1.1,
            "UNDERPERFORMANCE": 0.9,
            "PATTERN_BREAK": 0.6,
            "DOWNTIME": 2.0,  # Full downtime is most expensive
        }
    
    def calculate(
        self,
        anomaly_type: str,
        source: str,
        duration_minutes: float,
        deviation_percent: float,
        cost_per_minute: float = 75.0,
        industry: str = "MANUFACTURING",
    ) -> Dict[str, Any]:
        """
        Calculate the estimated monetary loss from an inefficiency.
        
        Args:
            anomaly_type: Type of anomaly (e.g., IDLE_SPIKE, THROUGHPUT_DROP)
            source: Source of the anomaly (e.g., machine-1, shift-A)
            duration_minutes: Duration of the inefficiency in minutes
            deviation_percent: Percentage deviation from expected
            cost_per_minute: Base operational cost per minute
            industry: Industry type for multiplier adjustment
        
        Returns:
            Dictionary with loss breakdown and methodology
        """
        # Get multipliers
        industry_mult = self.industry_multipliers.get(industry, 1.0)
        anomaly_weight = self.anomaly_weights.get(anomaly_type, 1.0)
        
        # Calculate base loss
        # loss = deviation_impact × duration × cost × multipliers
        deviation_impact = abs(deviation_percent) / 100
        
        base_loss = deviation_impact * duration_minutes * cost_per_minute
        adjusted_loss = base_loss * industry_mult * anomaly_weight
        
        # Calculate breakdown
        breakdown = {
            "base_loss": round(base_loss, 2),
            "industry_adjustment": round(base_loss * (industry_mult - 1), 2),
            "severity_adjustment": round(base_loss * industry_mult * (anomaly_weight - 1), 2),
        }
        
        # Calculate confidence based on data quality
        confidence = self._calculate_confidence(
            deviation_percent, duration_minutes, anomaly_type
        )
        
        return {
            "estimated_loss": round(adjusted_loss, 2),
            "currency": "INR",
            "breakdown": breakdown,
            "confidence": confidence,
            "methodology": self._get_methodology(anomaly_type),
        }
    
    def calculate_batch(
        self,
        anomalies: list,
        cost_per_minute: float = 75.0,
        industry: str = "MANUFACTURING",
    ) -> Dict[str, Any]:
        """
        Calculate total loss for multiple anomalies.
        """
        total_loss = 0
        by_type = {}
        by_source = {}
        
        for anomaly in anomalies:
            result = self.calculate(
                anomaly_type=anomaly.get("anomaly_type", "UNKNOWN"),
                source=anomaly.get("source", "unknown"),
                duration_minutes=anomaly.get("duration_minutes", 30),
                deviation_percent=anomaly.get("deviation_percent", 10),
                cost_per_minute=cost_per_minute,
                industry=industry,
            )
            
            loss = result["estimated_loss"]
            total_loss += loss
            
            atype = anomaly.get("anomaly_type", "UNKNOWN")
            source = anomaly.get("source", "unknown")
            
            by_type[atype] = by_type.get(atype, 0) + loss
            by_source[source] = by_source.get(source, 0) + loss
        
        return {
            "total_loss": round(total_loss, 2),
            "currency": "INR",
            "by_type": {k: round(v, 2) for k, v in by_type.items()},
            "by_source": {k: round(v, 2) for k, v in by_source.items()},
            "count": len(anomalies),
        }
    
    def estimate_recovery(
        self,
        current_loss: float,
        optimization_type: str,
    ) -> Dict[str, Any]:
        """
        Estimate potential recovery from an optimization action.
        """
        recovery_rates = {
            "REBALANCE_WORKLOAD": 0.65,
            "SCHEDULE_MAINTENANCE": 0.80,
            "ADJUST_ROUTING": 0.50,
            "TRAINING_NEEDED": 0.40,
            "RESOURCE_ALLOCATION": 0.70,
            "ALERT_SUPERVISOR": 0.30,
            "MODIFY_PROCESS": 0.55,
        }
        
        rate = recovery_rates.get(optimization_type, 0.5)
        
        return {
            "estimated_recovery": round(current_loss * rate, 2),
            "recovery_rate": rate,
            "residual_loss": round(current_loss * (1 - rate), 2),
        }
    
    def _calculate_confidence(
        self,
        deviation: float,
        duration: float,
        anomaly_type: str,
    ) -> float:
        """Calculate confidence score for the loss estimate."""
        base_confidence = 0.85
        
        # Higher deviation = slightly lower confidence (more uncertainty)
        if abs(deviation) > 50:
            base_confidence -= 0.1
        elif abs(deviation) > 30:
            base_confidence -= 0.05
        
        # Very short durations have higher uncertainty
        if duration < 5:
            base_confidence -= 0.1
        elif duration < 15:
            base_confidence -= 0.05
        
        # Some anomaly types are harder to quantify
        uncertain_types = ["PATTERN_BREAK", "UNDERPERFORMANCE"]
        if anomaly_type in uncertain_types:
            base_confidence -= 0.1
        
        return round(max(0.5, min(0.95, base_confidence)), 2)
    
    def _get_methodology(self, anomaly_type: str) -> str:
        """Return the calculation methodology description."""
        methodologies = {
            "IDLE_SPIKE": "Calculated based on productive time lost during idle periods",
            "THROUGHPUT_DROP": "Based on reduced output rate vs expected production",
            "MACHINE_SLOWDOWN": "Calculated from machine efficiency degradation",
            "QUALITY_DECLINE": "Includes rework costs and potential scrap value",
            "DOWNTIME": "Full production loss for downtime duration",
            "OVERLOAD": "Efficiency loss due to resource saturation",
        }
        
        return methodologies.get(
            anomaly_type,
            "Standard loss calculation: deviation × duration × cost × adjustments"
        )
