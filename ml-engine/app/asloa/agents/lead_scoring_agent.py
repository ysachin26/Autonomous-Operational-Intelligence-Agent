"""
ASLOA - Lead Scoring Agent
Scores incoming leads 0-100 based on ICP (Ideal Customer Profile) fit.

Scoring Criteria:
- Company size & revenue
- Industry alignment
- Job title authority
- Engagement signals
- Historical conversion patterns
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
import random

from app.agents.base_agent import BaseAgent


class LeadScoringAgent(BaseAgent):
    """
    Lead Scoring Agent - Scores leads from 0-100 based on ICP fit.
    
    High scores (80-100): Hot leads, immediate priority
    Medium scores (60-79): Warm leads, nurture worthy
    Low scores (40-59): Cold leads, qualification needed
    Very low (<40): Likely not a fit, deprioritize
    """
    
    def __init__(self):
        super().__init__("lead_scoring")
        
        # ICP (Ideal Customer Profile) weights
        self.icp_weights = {
            "company_size": 20,      # 0-20 points
            "industry_fit": 20,      # 0-20 points
            "authority_level": 20,   # 0-20 points
            "engagement": 20,        # 0-20 points
            "budget_signals": 20,    # 0-20 points
        }
        
        # Ideal company sizes by revenue tier
        self.ideal_company_sizes = {
            "enterprise": {"min": 1000, "max": float("inf"), "score": 20},
            "mid_market": {"min": 100, "max": 999, "score": 18},
            "smb": {"min": 20, "max": 99, "score": 12},
            "startup": {"min": 1, "max": 19, "score": 8},
        }
        
        # Target industries
        self.target_industries = {
            "technology": 20,
            "saas": 20,
            "fintech": 18,
            "healthcare": 16,
            "manufacturing": 15,
            "retail": 14,
            "ecommerce": 14,
            "logistics": 13,
            "education": 12,
            "other": 8,
        }
        
        # Authority levels
        self.authority_levels = {
            "c_level": 20,        # CEO, CTO, CFO, etc.
            "vp": 18,             # VP of Sales, VP Engineering
            "director": 16,       # Director level
            "manager": 12,        # Manager level
            "individual": 6,      # IC
            "unknown": 4,
        }
    
    def process(
        self, 
        input_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Score a lead based on ICP criteria.
        
        Input:
        - lead_id: Unique identifier
        - company: Company name
        - company_size: Number of employees
        - industry: Industry vertical
        - contact_name: Contact name
        - contact_title: Job title
        - contact_email: Email address
        - source: Lead source (website, linkedin, referral, etc.)
        - engagement_signals: List of engagement events
        - budget_mentioned: Boolean
        - annual_revenue: Optional revenue estimate
        """
        start_time = self._start_processing()
        
        try:
            lead_id = input_data.get("lead_id", f"lead-{uuid.uuid4().hex[:8]}")
            
            # Calculate component scores
            company_score = self._score_company_size(input_data)
            industry_score = self._score_industry(input_data)
            authority_score = self._score_authority(input_data)
            engagement_score = self._score_engagement(input_data)
            budget_score = self._score_budget_signals(input_data)
            
            # Total score
            total_score = (
                company_score + 
                industry_score + 
                authority_score + 
                engagement_score + 
                budget_score
            )
            
            # Determine lead tier
            if total_score >= 80:
                tier = "HOT"
                priority = "immediate"
                recommendation = "Prioritize for immediate outreach"
            elif total_score >= 60:
                tier = "WARM"
                priority = "high"
                recommendation = "Add to nurture sequence"
            elif total_score >= 40:
                tier = "COLD"
                priority = "normal"
                recommendation = "Qualify further before outreach"
            else:
                tier = "UNQUALIFIED"
                priority = "low"
                recommendation = "Likely not a fit, consider deprioritizing"
            
            result = {
                "lead_id": lead_id,
                "score": total_score,
                "tier": tier,
                "priority": priority,
                "recommendation": recommendation,
                "breakdown": {
                    "company_size_score": company_score,
                    "industry_score": industry_score,
                    "authority_score": authority_score,
                    "engagement_score": engagement_score,
                    "budget_signals_score": budget_score,
                },
                "reasoning": self._generate_reasoning(
                    input_data, total_score, tier,
                    company_score, industry_score, authority_score,
                    engagement_score, budget_score
                ),
                "scored_at": datetime.now().isoformat(),
            }
            
            self._complete_processing(start_time, success=True)
            self._last_output = result
            
            return {
                "status": "success",
                "scoring": result,
            }
            
        except Exception as e:
            self._log_error(e, "Lead scoring failed")
            self._complete_processing(start_time, success=False)
            return {"status": "error", "error": str(e)}
    
    def _score_company_size(self, lead: Dict) -> int:
        """Score based on company size/employees."""
        size = lead.get("company_size", 0)
        
        if size >= 1000:
            return 20
        elif size >= 100:
            return 18
        elif size >= 20:
            return 12
        elif size >= 1:
            return 8
        else:
            return 5  # Unknown size
    
    def _score_industry(self, lead: Dict) -> int:
        """Score based on industry fit."""
        industry = lead.get("industry", "other").lower()
        return self.target_industries.get(industry, 8)
    
    def _score_authority(self, lead: Dict) -> int:
        """Score based on contact's authority level."""
        title = lead.get("contact_title", "").lower()
        
        if any(x in title for x in ["ceo", "cto", "cfo", "coo", "chief", "founder", "owner"]):
            return 20
        elif any(x in title for x in ["vp", "vice president", "head of"]):
            return 18
        elif "director" in title:
            return 16
        elif "manager" in title:
            return 12
        elif any(x in title for x in ["lead", "senior"]):
            return 10
        else:
            return 6
    
    def _score_engagement(self, lead: Dict) -> int:
        """Score based on engagement signals."""
        signals = lead.get("engagement_signals", [])
        source = lead.get("source", "").lower()
        
        score = 0
        
        # Source scoring
        if source in ["referral", "partner"]:
            score += 8
        elif source in ["demo_request", "contact_form"]:
            score += 7
        elif source == "linkedin":
            score += 5
        elif source == "website":
            score += 4
        elif source in ["ad", "paid"]:
            score += 3
        else:
            score += 2
        
        # Engagement signals
        if "pricing_page_visit" in signals:
            score += 4
        if "demo_watched" in signals:
            score += 4
        if "case_study_download" in signals:
            score += 3
        if "email_opened" in signals:
            score += 2
        if "email_clicked" in signals:
            score += 3
        
        return min(score, 20)
    
    def _score_budget_signals(self, lead: Dict) -> int:
        """Score based on budget indicators."""
        score = 0
        
        if lead.get("budget_mentioned"):
            score += 10
        
        revenue = lead.get("annual_revenue", 0)
        if revenue >= 10_000_000:
            score += 10
        elif revenue >= 1_000_000:
            score += 8
        elif revenue >= 100_000:
            score += 5
        elif revenue > 0:
            score += 3
        
        if lead.get("funding_raised"):
            score += 5
        
        return min(score, 20)
    
    def _generate_reasoning(
        self, lead: Dict, total: int, tier: str,
        company: int, industry: int, authority: int,
        engagement: int, budget: int
    ) -> str:
        """Generate human-readable scoring reasoning."""
        company_name = lead.get("company", "the company")
        contact = lead.get("contact_name", "the contact")
        title = lead.get("contact_title", "")
        
        reasons = []
        
        # Highlight strengths
        if authority >= 16:
            reasons.append(f"{contact} ({title}) is a decision-maker")
        if company >= 18:
            reasons.append(f"{company_name} is in our ideal company size range")
        if industry >= 16:
            reasons.append(f"Industry is a strong fit for our solution")
        if engagement >= 12:
            reasons.append(f"Shows high engagement signals")
        if budget >= 12:
            reasons.append(f"Budget indicators are positive")
        
        # Highlight weaknesses
        if authority < 10:
            reasons.append(f"Contact may not be a decision-maker")
        if company < 10:
            reasons.append(f"Company size is below ideal range")
        if engagement < 8:
            reasons.append(f"Limited engagement activity")
        
        reasoning = f"Lead scored {total}/100 ({tier}). "
        if reasons:
            reasoning += " | ".join(reasons[:3])
        
        return reasoning
