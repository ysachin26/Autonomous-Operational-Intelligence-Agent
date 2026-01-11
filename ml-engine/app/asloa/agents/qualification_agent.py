"""
ASLOA - Qualification Agent
Qualifies leads using BANT framework.

BANT:
- Budget: Can they afford the solution?
- Authority: Is this the decision maker?
- Need: Do they have a pain point we solve?
- Timeline: What's their buying timeline?
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

from app.agents.base_agent import BaseAgent


class QualificationAgent(BaseAgent):
    """
    Qualification Agent - BANT-based lead qualification.
    
    Returns qualification status:
    - QUALIFIED: All BANT criteria met
    - PARTIALLY_QUALIFIED: 2-3 criteria met
    - NEEDS_NURTURING: 1-2 criteria met
    - DISQUALIFIED: 0-1 criteria met
    """
    
    def __init__(self):
        super().__init__("qualification")
        
        # BANT thresholds
        self.thresholds = {
            "min_budget": 10000,          # Minimum budget in USD
            "authority_keywords": [
                "ceo", "cto", "cfo", "coo", "founder", "owner",
                "chief", "vp", "vice president", "head of",
                "director", "manager", "decision"
            ],
            "need_keywords": [
                "problem", "challenge", "pain", "issue", "struggle",
                "looking for", "need", "want", "require", "improve",
                "automate", "efficiency", "cost", "revenue", "growth"
            ],
            "urgent_timeline_days": 90,   # Within 3 months = urgent
        }
    
    def process(
        self,
        input_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Qualify a lead using BANT framework.
        
        Input:
        - lead_id: Lead identifier
        - budget: Estimated budget or None
        - budget_confirmed: Whether budget was explicitly confirmed
        - contact_title: Job title of contact
        - is_decision_maker: Boolean if known
        - pain_points: List of identified pain points
        - needs_description: Text describing their needs
        - timeline: Expected buying timeline (days or text)
        - urgency_signals: List of urgency indicators
        """
        start_time = self._start_processing()
        
        try:
            lead_id = input_data.get("lead_id", f"lead-{uuid.uuid4().hex[:8]}")
            
            # Evaluate each BANT component
            budget_result = self._evaluate_budget(input_data)
            authority_result = self._evaluate_authority(input_data)
            need_result = self._evaluate_need(input_data)
            timeline_result = self._evaluate_timeline(input_data)
            
            # Count qualified criteria
            qualified_count = sum([
                budget_result["qualified"],
                authority_result["qualified"],
                need_result["qualified"],
                timeline_result["qualified"],
            ])
            
            # Determine status
            if qualified_count == 4:
                status = "QUALIFIED"
                action = "Move to sales engagement"
                confidence = 0.95
            elif qualified_count >= 3:
                status = "PARTIALLY_QUALIFIED"
                action = "Schedule discovery call to fill gaps"
                confidence = 0.80
            elif qualified_count >= 2:
                status = "NEEDS_NURTURING"
                action = "Add to nurture sequence"
                confidence = 0.60
            else:
                status = "DISQUALIFIED"
                action = "Deprioritize or remove from pipeline"
                confidence = 0.40
            
            # Generate next steps
            next_steps = self._generate_next_steps(
                budget_result, authority_result, 
                need_result, timeline_result
            )
            
            result = {
                "lead_id": lead_id,
                "qualification_status": status,
                "qualified_criteria": qualified_count,
                "total_criteria": 4,
                "confidence": confidence,
                "recommended_action": action,
                "bant_analysis": {
                    "budget": budget_result,
                    "authority": authority_result,
                    "need": need_result,
                    "timeline": timeline_result,
                },
                "next_steps": next_steps,
                "qualified_at": datetime.now().isoformat(),
            }
            
            self._complete_processing(start_time, success=True)
            self._last_output = result
            
            return {
                "status": "success",
                "qualification": result,
            }
            
        except Exception as e:
            self._log_error(e, "Qualification failed")
            self._complete_processing(start_time, success=False)
            return {"status": "error", "error": str(e)}
    
    def _evaluate_budget(self, lead: Dict) -> Dict[str, Any]:
        """Evaluate budget qualification."""
        budget = lead.get("budget", 0)
        budget_confirmed = lead.get("budget_confirmed", False)
        
        if budget_confirmed and budget >= self.thresholds["min_budget"]:
            return {
                "qualified": True,
                "score": 100,
                "reason": f"Budget of ${budget:,} confirmed",
            }
        elif budget >= self.thresholds["min_budget"]:
            return {
                "qualified": True,
                "score": 80,
                "reason": f"Estimated budget of ${budget:,} meets threshold",
            }
        elif budget > 0:
            return {
                "qualified": False,
                "score": 40,
                "reason": f"Budget of ${budget:,} below threshold",
                "gap": f"Need to confirm budget >= ${self.thresholds['min_budget']:,}",
            }
        else:
            return {
                "qualified": False,
                "score": 20,
                "reason": "Budget unknown",
                "gap": "Need to discover budget during call",
            }
    
    def _evaluate_authority(self, lead: Dict) -> Dict[str, Any]:
        """Evaluate authority/decision-maker status."""
        title = lead.get("contact_title", "").lower()
        is_dm = lead.get("is_decision_maker", None)
        
        if is_dm is True:
            return {
                "qualified": True,
                "score": 100,
                "reason": "Confirmed decision maker",
            }
        
        has_authority_title = any(
            kw in title for kw in self.thresholds["authority_keywords"]
        )
        
        if has_authority_title:
            return {
                "qualified": True,
                "score": 85,
                "reason": f"Title '{lead.get('contact_title', '')}' suggests decision-making authority",
            }
        else:
            return {
                "qualified": False,
                "score": 30,
                "reason": "Contact may not be decision maker",
                "gap": "Need to identify & engage decision maker",
            }
    
    def _evaluate_need(self, lead: Dict) -> Dict[str, Any]:
        """Evaluate if there's a clear need."""
        pain_points = lead.get("pain_points", [])
        needs_desc = lead.get("needs_description", "").lower()
        
        has_pain = len(pain_points) > 0
        has_keywords = any(
            kw in needs_desc for kw in self.thresholds["need_keywords"]
        )
        
        if has_pain and len(pain_points) >= 2:
            return {
                "qualified": True,
                "score": 100,
                "reason": f"Clear need identified: {', '.join(pain_points[:3])}",
            }
        elif has_pain or has_keywords:
            return {
                "qualified": True,
                "score": 75,
                "reason": "Need indicators present",
            }
        else:
            return {
                "qualified": False,
                "score": 25,
                "reason": "No clear need identified",
                "gap": "Need to uncover pain points during discovery",
            }
    
    def _evaluate_timeline(self, lead: Dict) -> Dict[str, Any]:
        """Evaluate buying timeline."""
        timeline = lead.get("timeline")  # Can be days or text
        urgency = lead.get("urgency_signals", [])
        
        # Handle numeric timeline
        if isinstance(timeline, (int, float)):
            if timeline <= self.thresholds["urgent_timeline_days"]:
                return {
                    "qualified": True,
                    "score": 100,
                    "reason": f"Buying timeline within {int(timeline)} days",
                }
            elif timeline <= 180:
                return {
                    "qualified": True,
                    "score": 70,
                    "reason": f"Timeline of {int(timeline)} days - active evaluation",
                }
            else:
                return {
                    "qualified": False,
                    "score": 30,
                    "reason": f"Long timeline of {int(timeline)} days",
                    "gap": "Keep warm for future engagement",
                }
        
        # Handle urgency signals
        if urgency and len(urgency) > 0:
            return {
                "qualified": True,
                "score": 80,
                "reason": f"Urgency signals: {', '.join(urgency[:2])}",
            }
        
        return {
            "qualified": False,
            "score": 20,
            "reason": "Timeline unknown",
            "gap": "Need to establish timeline expectation",
        }
    
    def _generate_next_steps(
        self, budget: Dict, authority: Dict, need: Dict, timeline: Dict
    ) -> List[str]:
        """Generate actionable next steps based on gaps."""
        steps = []
        
        if not budget["qualified"]:
            steps.append("Discover budget during qualification call")
        if not authority["qualified"]:
            steps.append("Identify and engage the decision maker")
        if not need["qualified"]:
            steps.append("Conduct discovery to uncover pain points")
        if not timeline["qualified"]:
            steps.append("Establish buying timeline and urgency")
        
        if not steps:
            steps.append("Schedule demo with sales team")
            steps.append("Prepare custom proposal")
        
        return steps
