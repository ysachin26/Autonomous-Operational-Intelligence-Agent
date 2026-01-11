"""
AOIA ML Engine - Loss Estimation Agent
Computes monetary impact of operational inefficiencies.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

from app.agents.base_agent import BaseAgent
from app.services.loss_calculator import LossCalculator
from app.models.output_schemas import FinancialLoss, LossBreakdown


class LossEstimationAgent(BaseAgent):
    """
    Loss Estimation Agent - Computes money lost from inefficiencies.
    
    Inputs: Anomalies, baselines, cost parameters
    Outputs: Monetary loss with projections and savings potential
    """
    
    def __init__(self):
        super().__init__("loss_estimation")
        self.calculator = LossCalculator()
        
        # Default parameters
        self.default_cost_per_min = 75.0  # INR
        self.default_industry = "MANUFACTURING"
        
        # Historical data for projections
        self.historical_losses: List[float] = []
    
    def process(
        self, 
        input_data: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Calculate financial loss from detected inefficiencies.
        
        Args:
            input_data: Contains detections and business parameters
            context: Optional - additional calculation context
            
        Returns:
            FinancialLoss with breakdown and projections
        """
        start_time = self._start_processing()
        
        try:
            detections = input_data.get("detections", [])
            business = input_data.get("business", {})
            
            cost_per_min = business.get("cost_per_min", self.default_cost_per_min)
            industry = business.get("industry", self.default_industry)
            baseline_output = business.get("baseline_output_per_min", 10)
            
            # Calculate losses for each detection
            individual_losses = []
            total_loss = 0
            by_type: Dict[str, float] = {}
            by_source: Dict[str, float] = {}
            
            for detection in detections:
                loss_result = self._calculate_detection_loss(
                    detection, cost_per_min, industry
                )
                individual_losses.append(loss_result)
                total_loss += loss_result["estimated_loss"]
                
                # Aggregate by type
                atype = detection.get("anomaly_type", "UNKNOWN")
                by_type[atype] = by_type.get(atype, 0) + loss_result["estimated_loss"]
                
                # Aggregate by source
                source = detection.get("anomaly_location", "unknown")
                by_source[source] = by_source.get(source, 0) + loss_result["estimated_loss"]
            
            # Calculate projections
            duration_mins = self._estimate_total_duration(detections)
            money_per_min = total_loss / max(duration_mins, 1)
            
            # Project future loss (24 hours if not fixed)
            projected_24h = money_per_min * 60 * 24
            
            # Calculate savings potential
            savings = self._calculate_savings_potential(total_loss, detections)
            
            # Build confidence score
            confidence = self._calculate_overall_confidence(individual_losses, detections)
            
            # Create breakdown
            breakdown = LossBreakdown(
                base_loss=sum(l.get("breakdown", {}).get("base_loss", 0) for l in individual_losses),
                industry_adjustment=sum(l.get("breakdown", {}).get("industry_adjustment", 0) for l in individual_losses),
                severity_adjustment=sum(l.get("breakdown", {}).get("severity_adjustment", 0) for l in individual_losses),
            )
            
            # Build financial loss output
            financial_loss = FinancialLoss(
                total_loss=round(total_loss, 2),
                currency="INR",
                money_lost_per_min=round(money_per_min, 2),
                money_lost_total=round(total_loss, 2),
                projected_future_loss=round(projected_24h, 2),
                savings_if_fixed=round(savings, 2),
                breakdown=breakdown,
                by_type={k: round(v, 2) for k, v in by_type.items()},
                by_source={k: round(v, 2) for k, v in by_source.items()},
                confidence=confidence,
                methodology=self._get_methodology_summary(detections),
                timestamp=datetime.now(),
            )
            
            # Track historical
            self.historical_losses.append(total_loss)
            if len(self.historical_losses) > 100:
                self.historical_losses = self.historical_losses[-100:]
            
            self._complete_processing(start_time, success=True)
            
            return {
                "status": "success",
                "financial_loss": financial_loss.model_dump(),
                "individual_losses": individual_losses,
                "processing_time_ms": (datetime.now() - start_time).total_seconds() * 1000,
            }
            
        except Exception as e:
            self._log_error(e, "Loss estimation failed")
            self._complete_processing(start_time, success=False)
            return {"status": "error", "error": str(e)}
    
    def _calculate_detection_loss(
        self, 
        detection: Dict[str, Any],
        cost_per_min: float,
        industry: str
    ) -> Dict[str, Any]:
        """Calculate loss for a single detection."""
        anomaly_type = detection.get("anomaly_type", "UNKNOWN")
        source = detection.get("anomaly_location", "unknown")
        deviation = detection.get("deviation_percent", 10)
        
        # Estimate duration from detection or default
        duration = detection.get("duration_minutes", 30)
        
        return self.calculator.calculate(
            anomaly_type=anomaly_type,
            source=source,
            duration_minutes=duration,
            deviation_percent=deviation,
            cost_per_minute=cost_per_min,
            industry=industry,
        )
    
    def _estimate_total_duration(self, detections: List[Dict]) -> float:
        """Estimate total duration of all inefficiencies."""
        total = 0
        for d in detections:
            total += d.get("duration_minutes", 30)
        return max(total, 1)
    
    def _calculate_savings_potential(
        self, 
        total_loss: float, 
        detections: List[Dict]
    ) -> float:
        """Calculate potential savings if issues are fixed."""
        # Different fix rates for different anomaly types
        fix_rates = {
            "IDLE_SPIKE": 0.75,
            "THROUGHPUT_DROP": 0.65,
            "MICRO_DOWNTIME": 0.80,
            "DOWNTIME": 0.90,
            "REWORK_LOOPS": 0.60,
            "EXCESSIVE_HANDOVERS": 0.50,
            "OPERATOR_OVERLOAD": 0.55,
            "UNDERUTILIZATION": 0.70,
            "IDLE_TIME_SPIKE": 0.65,
        }
        
        # Weight by detection type
        weighted_rate = 0.65  # Default
        if detections:
            total_weight = 0
            weighted_sum = 0
            for d in detections:
                atype = d.get("anomaly_type", "UNKNOWN")
                rate = fix_rates.get(atype, 0.50)
                severity = d.get("severity_score", 0.5)
                weight = severity
                weighted_sum += rate * weight
                total_weight += weight
            
            if total_weight > 0:
                weighted_rate = weighted_sum / total_weight
        
        return total_loss * weighted_rate
    
    def _calculate_overall_confidence(
        self, 
        individual_losses: List[Dict],
        detections: List[Dict]
    ) -> float:
        """Calculate overall confidence score."""
        if not individual_losses:
            return 0.5
        
        confidences = [l.get("confidence", 0.7) for l in individual_losses]
        avg_confidence = sum(confidences) / len(confidences)
        
        # Adjust for number of detections (more data = higher confidence)
        detection_factor = min(len(detections) / 10, 1.0) * 0.1
        
        return min(avg_confidence + detection_factor, 0.95)
    
    def _get_methodology_summary(self, detections: List[Dict]) -> str:
        """Get summary of calculation methodology."""
        types = set(d.get("anomaly_type", "") for d in detections)
        if "DOWNTIME" in types:
            return "Loss calculated from full production halt and partial slowdowns"
        elif "THROUGHPUT_DROP" in types:
            return "Loss calculated from reduced output rate vs expected production"
        elif "IDLE_SPIKE" in types:
            return "Loss calculated from productive time lost during idle periods"
        else:
            return "Standard loss calculation: deviation × duration × cost × adjustments"
    
    def get_historical_trend(self) -> Dict[str, Any]:
        """Get historical loss trend."""
        if not self.historical_losses:
            return {"trend": "no_data", "average": 0}
        
        avg = sum(self.historical_losses) / len(self.historical_losses)
        recent_avg = sum(self.historical_losses[-10:]) / min(len(self.historical_losses), 10)
        
        if recent_avg > avg * 1.1:
            trend = "increasing"
        elif recent_avg < avg * 0.9:
            trend = "decreasing"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "average": round(avg, 2),
            "recent_average": round(recent_avg, 2),
            "data_points": len(self.historical_losses),
        }
