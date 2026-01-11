"""
ASLOA - Analytics Agent
Sales intelligence and forecasting.

Capabilities:
- Conversion tracking
- Deal probability
- Revenue forecasting
- Rep performance metrics
- Time saved calculations
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import uuid

from app.agents.base_agent import BaseAgent


class AnalyticsAgent(BaseAgent):
    """
    Analytics Agent - Sales metrics and forecasting.
    
    Tracks:
    - Pipeline metrics
    - Conversion rates
    - Rep performance
    - Revenue forecasting
    - ASLOA efficiency gains
    """
    
    def __init__(self):
        super().__init__("analytics")
        
        # Historical metrics (simulated)
        self.pipeline_data = {
            "total_leads": 0,
            "leads_by_tier": {"HOT": 0, "WARM": 0, "COLD": 0},
            "leads_by_status": {},
            "total_value": 0,
            "weighted_value": 0,
        }
        
        self.conversion_rates = {
            "lead_to_qualified": 0.35,
            "qualified_to_demo": 0.50,
            "demo_to_proposal": 0.60,
            "proposal_to_closed": 0.40,
            "overall": 0.042,  # ~4.2% lead to close
        }
        
        # Time tracking
        self.time_saved = {
            "scoring_hours": 0,
            "research_hours": 0,
            "email_hours": 0,
            "routing_hours": 0,
            "crm_hours": 0,
        }
    
    def process(
        self,
        input_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate analytics for a processed lead.
        
        Input:
        - lead_id: Lead identifier
        - score: Lead score
        - lead_tier: HOT/WARM/COLD
        - qualification: Qualification result
        - deal_size_estimate: Deal value
        - processing_steps: List of completed steps
        """
        start_time = self._start_processing()
        
        try:
            lead_id = input_data.get("lead_id", f"lead-{uuid.uuid4().hex[:8]}")
            
            # Update pipeline metrics
            pipeline_update = self._update_pipeline_metrics(input_data)
            
            # Calculate conversion probability
            conversion = self._calculate_conversion_probability(input_data)
            
            # Calculate time saved
            time_saved = self._calculate_time_saved(input_data)
            
            # Generate forecast impact
            forecast = self._generate_forecast_impact(input_data)
            
            # Rep performance impact
            rep_metrics = self._calculate_rep_impact(input_data)
            
            result = {
                "lead_id": lead_id,
                "pipeline_metrics": pipeline_update,
                "conversion_probability": conversion,
                "time_saved": time_saved,
                "forecast_impact": forecast,
                "rep_metrics": rep_metrics,
                "dashboard_summary": self._generate_dashboard_summary(
                    pipeline_update, conversion, time_saved, forecast
                ),
                "analyzed_at": datetime.now().isoformat(),
            }
            
            self._complete_processing(start_time, success=True)
            self._last_output = result
            
            return {
                "status": "success",
                "analytics": result,
            }
            
        except Exception as e:
            self._log_error(e, "Analytics failed")
            self._complete_processing(start_time, success=False)
            return {"status": "error", "error": str(e)}
    
    def _update_pipeline_metrics(self, data: Dict) -> Dict[str, Any]:
        """Update and return pipeline metrics."""
        tier = data.get("lead_tier", "COLD")
        deal_value = data.get("deal_size_estimate", 0)
        qualification = data.get("qualification", {})
        qual_status = qualification.get("qualification_status", "PENDING")
        
        # Update counts
        self.pipeline_data["total_leads"] += 1
        self.pipeline_data["leads_by_tier"][tier] = self.pipeline_data["leads_by_tier"].get(tier, 0) + 1
        self.pipeline_data["leads_by_status"][qual_status] = self.pipeline_data["leads_by_status"].get(qual_status, 0) + 1
        self.pipeline_data["total_value"] += deal_value
        
        # Calculate weighted value
        probability_map = {
            "QUALIFIED": 0.25,
            "PARTIALLY_QUALIFIED": 0.15,
            "NEEDS_NURTURING": 0.08,
            "DISQUALIFIED": 0.02,
        }
        probability = probability_map.get(qual_status, 0.05)
        weighted = deal_value * probability
        self.pipeline_data["weighted_value"] += weighted
        
        return {
            "lead_added": True,
            "tier": tier,
            "deal_value": deal_value,
            "weighted_value": weighted,
            "pipeline_totals": {
                "total_leads": self.pipeline_data["total_leads"],
                "total_value": self.pipeline_data["total_value"],
                "weighted_pipeline": self.pipeline_data["weighted_value"],
                "by_tier": self.pipeline_data["leads_by_tier"],
            },
        }
    
    def _calculate_conversion_probability(self, data: Dict) -> Dict[str, Any]:
        """Calculate this lead's conversion probability."""
        score = data.get("score", 50)
        tier = data.get("lead_tier", "COLD")
        qualification = data.get("qualification", {})
        qual_status = qualification.get("qualification_status", "PENDING")
        
        # Base probability from score
        base_prob = score / 100 * 0.1  # 100 score = 10% base
        
        # Tier modifier
        tier_modifiers = {"HOT": 2.5, "WARM": 1.5, "COLD": 1.0}
        tier_prob = base_prob * tier_modifiers.get(tier, 1.0)
        
        # Qualification modifier
        qual_modifiers = {
            "QUALIFIED": 2.0,
            "PARTIALLY_QUALIFIED": 1.5,
            "NEEDS_NURTURING": 0.8,
            "DISQUALIFIED": 0.3,
        }
        final_prob = tier_prob * qual_modifiers.get(qual_status, 1.0)
        
        # Cap at 50%
        final_prob = min(final_prob, 0.50)
        
        return {
            "probability": round(final_prob, 3),
            "confidence": 0.85,
            "factors": {
                "score_contribution": round(base_prob, 3),
                "tier_multiplier": tier_modifiers.get(tier, 1.0),
                "qualification_multiplier": qual_modifiers.get(qual_status, 1.0),
            },
            "comparable_leads": f"Similar leads convert at {round(final_prob * 100, 1)}%",
        }
    
    def _calculate_time_saved(self, data: Dict) -> Dict[str, Any]:
        """Calculate time saved by ASLOA automation."""
        # Time estimates (in minutes) that ASLOA saves
        time_savings = {
            "scoring": 15,      # Manual scoring takes ~15 min
            "research": 45,     # Manual research takes ~45 min
            "email_draft": 20,  # Writing personalized email takes ~20 min
            "routing": 10,      # Manual routing takes ~10 min
            "crm_update": 15,   # CRM data entry takes ~15 min
        }
        
        total_minutes = sum(time_savings.values())
        total_hours = total_minutes / 60
        
        # Update cumulative
        self.time_saved["scoring_hours"] += time_savings["scoring"] / 60
        self.time_saved["research_hours"] += time_savings["research"] / 60
        self.time_saved["email_hours"] += time_savings["email_draft"] / 60
        self.time_saved["routing_hours"] += time_savings["routing"] / 60
        self.time_saved["crm_hours"] += time_savings["crm_update"] / 60
        
        total_cumulative = sum(self.time_saved.values())
        
        # Calculate value
        hourly_cost = 50  # USD per hour for sales rep
        
        return {
            "this_lead_minutes": total_minutes,
            "this_lead_hours": round(total_hours, 2),
            "breakdown": time_savings,
            "cumulative_hours": round(total_cumulative, 2),
            "value_saved_usd": round(total_cumulative * hourly_cost, 2),
            "annualized_projection": {
                "hours_per_year": round(total_cumulative * 250, 0),  # 250 working days
                "value_per_year_usd": round(total_cumulative * 250 * hourly_cost, 0),
            },
        }
    
    def _generate_forecast_impact(self, data: Dict) -> Dict[str, Any]:
        """Generate revenue forecast impact."""
        deal_value = data.get("deal_size_estimate", 0)
        qualification = data.get("qualification", {})
        qual_status = qualification.get("qualification_status", "PENDING")
        
        # Close probability
        prob_map = {
            "QUALIFIED": 0.25,
            "PARTIALLY_QUALIFIED": 0.15,
            "NEEDS_NURTURING": 0.08,
            "DISQUALIFIED": 0.02,
        }
        probability = prob_map.get(qual_status, 0.05)
        
        expected_value = deal_value * probability
        
        # Confidence interval (simulation)
        low = expected_value * 0.7
        high = expected_value * 1.4
        
        return {
            "deal_value": deal_value,
            "close_probability": probability,
            "expected_revenue": round(expected_value, 2),
            "confidence_interval": {
                "low": round(low, 2),
                "high": round(high, 2),
                "confidence": 0.80,
            },
            "forecast_month": (datetime.now() + timedelta(days=90)).strftime("%B %Y"),
            "pipeline_contribution": "added",
        }
    
    def _calculate_rep_impact(self, data: Dict) -> Dict[str, Any]:
        """Calculate impact on rep metrics."""
        routing = data.get("routing", {})
        assigned_to = routing.get("assigned_to", {})
        
        if not assigned_to:
            return {"status": "no_assignment"}
        
        return {
            "rep_id": assigned_to.get("rep_id", ""),
            "rep_name": assigned_to.get("name", ""),
            "impact": {
                "pipeline_added": data.get("deal_size_estimate", 0),
                "leads_assigned_today": 1,  # Would be tracked cumulative
                "time_saved_hours": 1.75,
                "capacity_used": "+1 deal",
            },
        }
    
    def _generate_dashboard_summary(
        self,
        pipeline: Dict,
        conversion: Dict,
        time_saved: Dict,
        forecast: Dict
    ) -> Dict[str, Any]:
        """Generate summary for dashboard display."""
        return {
            "headline": f"Lead processed with {round(conversion['probability']*100, 1)}% win probability",
            "key_metrics": {
                "pipeline_value": f"${pipeline.get('deal_value', 0):,}",
                "weighted_value": f"${pipeline.get('weighted_value', 0):,.0f}",
                "win_probability": f"{conversion['probability']*100:.1f}%",
                "time_saved": f"{time_saved['this_lead_minutes']} minutes",
            },
            "insights": [
                f"Pipeline now at ${self.pipeline_data['weighted_value']:,.0f} weighted",
                f"Cumulative time saved: {time_saved['cumulative_hours']:.1f} hours",
                f"Expected close: {forecast['forecast_month']}",
            ],
        }
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get full dashboard data for UI."""
        return {
            "pipeline": self.pipeline_data,
            "time_saved": self.time_saved,
            "conversion_rates": self.conversion_rates,
            "generated_at": datetime.now().isoformat(),
        }
