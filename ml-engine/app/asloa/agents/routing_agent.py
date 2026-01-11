"""
ASLOA - Routing Agent
Smart lead assignment to best-fit sales reps.

Assignment Criteria:
- Rep win rate for similar deals
- Current capacity/workload
- Segment expertise
- Territory alignment
- Chemistry fit
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
import random

from app.agents.base_agent import BaseAgent


class RoutingAgent(BaseAgent):
    """
    Routing Agent - Routes leads to best-fit sales reps.
    
    Uses multiple factors to optimize assignment:
    - Historical win rate
    - Current workload
    - Industry expertise
    - Deal size experience
    """
    
    def __init__(self):
        super().__init__("routing")
        
        # Simulated sales team (in production, this would come from CRM)
        self.sales_team = [
            {
                "rep_id": "rep-001",
                "name": "Sarah Johnson",
                "email": "sarah@company.com",
                "current_deals": 12,
                "capacity": 20,
                "win_rate": 0.35,
                "specialties": ["enterprise", "technology", "saas"],
                "territories": ["north", "west"],
                "avg_deal_size": 75000,
            },
            {
                "rep_id": "rep-002",
                "name": "Raj Patel",
                "email": "raj@company.com",
                "current_deals": 8,
                "capacity": 15,
                "win_rate": 0.42,
                "specialties": ["mid_market", "fintech", "healthcare"],
                "territories": ["south", "east"],
                "avg_deal_size": 45000,
            },
            {
                "rep_id": "rep-003",
                "name": "Mike Chen",
                "email": "mike@company.com",
                "current_deals": 15,
                "capacity": 18,
                "win_rate": 0.38,
                "specialties": ["enterprise", "manufacturing", "retail"],
                "territories": ["west", "international"],
                "avg_deal_size": 120000,
            },
            {
                "rep_id": "rep-004",
                "name": "Priya Sharma",
                "email": "priya@company.com",
                "current_deals": 5,
                "capacity": 12,
                "win_rate": 0.48,
                "specialties": ["smb", "startup", "technology"],
                "territories": ["all"],
                "avg_deal_size": 25000,
            },
        ]
    
    def process(
        self,
        input_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Route lead to best-fit sales rep.
        
        Input:
        - lead_id: Lead identifier
        - company: Company name
        - company_size: Employee count
        - industry: Industry vertical
        - territory: Geographic region
        - deal_size_estimate: Estimated deal value
        - lead_tier: HOT, WARM, COLD
        - lead_score: 0-100 score
        """
        start_time = self._start_processing()
        
        try:
            lead_id = input_data.get("lead_id", f"lead-{uuid.uuid4().hex[:8]}")
            
            # Score each rep for this lead
            rep_scores = []
            for rep in self.sales_team:
                score = self._score_rep_for_lead(rep, input_data)
                rep_scores.append({
                    "rep": rep,
                    "score": score["total"],
                    "breakdown": score,
                })
            
            # Sort by score
            rep_scores.sort(key=lambda x: x["score"], reverse=True)
            
            # Select best rep
            best_match = rep_scores[0]
            backup_match = rep_scores[1] if len(rep_scores) > 1 else None
            
            # Generate assignment
            assignment = {
                "lead_id": lead_id,
                "assigned_to": {
                    "rep_id": best_match["rep"]["rep_id"],
                    "name": best_match["rep"]["name"],
                    "email": best_match["rep"]["email"],
                },
                "assignment_score": best_match["score"],
                "score_breakdown": best_match["breakdown"],
                "backup_rep": {
                    "rep_id": backup_match["rep"]["rep_id"],
                    "name": backup_match["rep"]["name"],
                } if backup_match else None,
                "reason": self._generate_assignment_reason(best_match, input_data),
                "expected_response_time": self._get_expected_response(
                    best_match["rep"], input_data.get("lead_tier", "COLD")
                ),
                "routed_at": datetime.now().isoformat(),
            }
            
            self._complete_processing(start_time, success=True)
            self._last_output = assignment
            
            return {
                "status": "success",
                "routing": assignment,
            }
            
        except Exception as e:
            self._log_error(e, "Routing failed")
            self._complete_processing(start_time, success=False)
            return {"status": "error", "error": str(e)}
    
    def _score_rep_for_lead(self, rep: Dict, lead: Dict) -> Dict[str, Any]:
        """Score a rep's fit for this lead."""
        scores = {
            "capacity": 0,
            "expertise": 0,
            "win_rate": 0,
            "deal_size_fit": 0,
            "territory": 0,
        }
        
        # Capacity score (0-25) - prefer reps with more bandwidth
        capacity_used = rep["current_deals"] / rep["capacity"]
        if capacity_used < 0.5:
            scores["capacity"] = 25
        elif capacity_used < 0.7:
            scores["capacity"] = 20
        elif capacity_used < 0.9:
            scores["capacity"] = 10
        else:
            scores["capacity"] = 5
        
        # Expertise score (0-25) - match industry/segment
        industry = lead.get("industry", "").lower()
        company_size = lead.get("company_size", 100)
        
        # Determine segment
        if company_size >= 1000:
            segment = "enterprise"
        elif company_size >= 100:
            segment = "mid_market"
        elif company_size >= 20:
            segment = "smb"
        else:
            segment = "startup"
        
        if industry in rep["specialties"]:
            scores["expertise"] += 15
        if segment in rep["specialties"]:
            scores["expertise"] += 10
        
        # Win rate score (0-20)
        scores["win_rate"] = int(rep["win_rate"] * 50)  # 0.4 win rate = 20 points
        
        # Deal size fit (0-15)
        deal_size = lead.get("deal_size_estimate", 50000)
        rep_avg = rep["avg_deal_size"]
        
        ratio = min(deal_size, rep_avg) / max(deal_size, rep_avg)
        scores["deal_size_fit"] = int(ratio * 15)
        
        # Territory (0-15)
        territory = lead.get("territory", "").lower()
        if "all" in rep["territories"] or territory in rep["territories"]:
            scores["territory"] = 15
        else:
            scores["territory"] = 5
        
        # Total
        scores["total"] = sum(scores.values())
        
        return scores
    
    def _generate_assignment_reason(self, match: Dict, lead: Dict) -> str:
        """Generate human-readable assignment reason."""
        rep = match["rep"]
        breakdown = match["breakdown"]
        
        reasons = []
        
        if breakdown["expertise"] >= 20:
            reasons.append(f"strong expertise in {lead.get('industry', 'this segment')}")
        if breakdown["capacity"] >= 20:
            reasons.append("has bandwidth for new deals")
        if breakdown["win_rate"] >= 15:
            reasons.append(f"{int(rep['win_rate']*100)}% win rate")
        
        if reasons:
            return f"Assigned to {rep['name']} because: {', '.join(reasons)}"
        else:
            return f"Assigned to {rep['name']} based on best available match"
    
    def _get_expected_response(self, rep: Dict, tier: str) -> str:
        """Get expected response time based on rep workload and lead tier."""
        capacity_used = rep["current_deals"] / rep["capacity"]
        
        if tier == "HOT":
            if capacity_used < 0.7:
                return "Within 5 minutes"
            else:
                return "Within 30 minutes"
        elif tier == "WARM":
            if capacity_used < 0.7:
                return "Within 2 hours"
            else:
                return "Within 4 hours"
        else:
            return "Within 24 hours"
