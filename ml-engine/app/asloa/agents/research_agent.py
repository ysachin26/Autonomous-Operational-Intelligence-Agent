"""
ASLOA - Research Agent
Deep prospect intelligence gathering.

Capabilities:
- Company profile analysis
- Buying committee mapping
- Decision-maker identification
- Pain point detection
- News & trigger events
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

from app.agents.base_agent import BaseAgent


class ResearchAgent(BaseAgent):
    """
    Research Agent - Gathers intelligence on prospects.
    
    Outputs:
    - Company profile (size, industry, tech stack)
    - Buying committee (stakeholders involved)
    - Pain points & opportunities
    - Recent news & triggers
    """
    
    def __init__(self):
        super().__init__("research")
        
        # Common pain points by industry
        self.industry_pain_points = {
            "technology": [
                "Scaling infrastructure",
                "Developer productivity",
                "Technical debt",
                "Security vulnerabilities",
            ],
            "saas": [
                "Customer churn",
                "User onboarding",
                "Feature prioritization",
                "Revenue expansion",
            ],
            "manufacturing": [
                "Operational efficiency",
                "Supply chain visibility",
                "Quality control",
                "Equipment downtime",
            ],
            "retail": [
                "Inventory management",
                "Customer experience",
                "Omnichannel integration",
                "Labor scheduling",
            ],
            "healthcare": [
                "Patient wait times",
                "Staff scheduling",
                "Compliance requirements",
                "Data interoperability",
            ],
            "fintech": [
                "Regulatory compliance",
                "Fraud detection",
                "Customer acquisition cost",
                "Operational risk",
            ],
        }
        
        # Typical buying committee roles
        self.committee_templates = {
            "enterprise": [
                {"role": "Economic Buyer", "typical_title": "CFO/VP Finance", "influence": "high"},
                {"role": "Technical Buyer", "typical_title": "CTO/VP Engineering", "influence": "high"},
                {"role": "User Buyer", "typical_title": "Director/Manager", "influence": "medium"},
                {"role": "Champion", "typical_title": "End User", "influence": "medium"},
                {"role": "Blocker", "typical_title": "IT Security/Procurement", "influence": "high"},
            ],
            "mid_market": [
                {"role": "Decision Maker", "typical_title": "CEO/Founder", "influence": "high"},
                {"role": "Technical Evaluator", "typical_title": "CTO/Tech Lead", "influence": "medium"},
                {"role": "User", "typical_title": "Team Lead", "influence": "low"},
            ],
            "smb": [
                {"role": "Owner/Decision Maker", "typical_title": "Founder/CEO", "influence": "high"},
            ],
        }
    
    def process(
        self,
        input_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Research a prospect organization.
        
        Input:
        - company: Company name
        - domain: Company website domain
        - industry: Industry vertical
        - company_size: Employee count
        - contact_name: Primary contact
        - contact_title: Contact's job title
        - contact_linkedin: LinkedIn URL (optional)
        - additional_contacts: List of other known contacts
        """
        start_time = self._start_processing()
        
        try:
            company = input_data.get("company", "Unknown Company")
            industry = input_data.get("industry", "technology").lower()
            size = input_data.get("company_size", 100)
            
            # Build company profile
            company_profile = self._build_company_profile(input_data)
            
            # Map buying committee
            buying_committee = self._map_buying_committee(input_data)
            
            # Identify pain points
            pain_points = self._identify_pain_points(input_data)
            
            # Generate trigger events (simulated)
            triggers = self._identify_triggers(input_data)
            
            # Generate personalization hooks
            personalization = self._generate_personalization_hooks(
                company_profile, pain_points, triggers
            )
            
            result = {
                "company": company,
                "company_profile": company_profile,
                "buying_committee": buying_committee,
                "pain_points": pain_points,
                "triggers": triggers,
                "personalization_hooks": personalization,
                "research_confidence": 0.75,
                "researched_at": datetime.now().isoformat(),
            }
            
            self._complete_processing(start_time, success=True)
            self._last_output = result
            
            return {
                "status": "success",
                "research": result,
            }
            
        except Exception as e:
            self._log_error(e, "Research failed")
            self._complete_processing(start_time, success=False)
            return {"status": "error", "error": str(e)}
    
    def _build_company_profile(self, lead: Dict) -> Dict[str, Any]:
        """Build comprehensive company profile."""
        size = lead.get("company_size", 100)
        
        # Determine company tier
        if size >= 1000:
            tier = "enterprise"
            revenue_estimate = f"${size * 150000:,}+"
        elif size >= 100:
            tier = "mid_market"
            revenue_estimate = f"${size * 100000:,} - ${size * 200000:,}"
        else:
            tier = "smb"
            revenue_estimate = f"${size * 50000:,} - ${size * 100000:,}"
        
        return {
            "name": lead.get("company", "Unknown"),
            "domain": lead.get("domain", ""),
            "industry": lead.get("industry", "technology"),
            "employee_count": size,
            "tier": tier,
            "revenue_estimate": revenue_estimate,
            "location": lead.get("location", "Unknown"),
            "founded": lead.get("founded", "Unknown"),
            "tech_stack": lead.get("tech_stack", []),
        }
    
    def _map_buying_committee(self, lead: Dict) -> List[Dict[str, Any]]:
        """Map the likely buying committee."""
        size = lead.get("company_size", 100)
        
        # Get template based on company size
        if size >= 1000:
            template = self.committee_templates["enterprise"]
        elif size >= 100:
            template = self.committee_templates["mid_market"]
        else:
            template = self.committee_templates["smb"]
        
        committee = []
        primary_contact = {
            "name": lead.get("contact_name", "Unknown"),
            "title": lead.get("contact_title", ""),
            "email": lead.get("contact_email", ""),
            "is_primary": True,
            "role": self._infer_role(lead.get("contact_title", "")),
            "influence": "high" if "chief" in lead.get("contact_title", "").lower() else "medium",
        }
        committee.append(primary_contact)
        
        # Add additional known contacts
        for contact in lead.get("additional_contacts", []):
            committee.append({
                "name": contact.get("name", "Unknown"),
                "title": contact.get("title", ""),
                "email": contact.get("email", ""),
                "is_primary": False,
                "role": self._infer_role(contact.get("title", "")),
                "influence": "medium",
            })
        
        # Add unknown stakeholders from template
        for template_role in template:
            if not any(c.get("role") == template_role["role"] for c in committee):
                committee.append({
                    "name": "To be identified",
                    "title": template_role["typical_title"],
                    "role": template_role["role"],
                    "influence": template_role["influence"],
                    "is_primary": False,
                    "needs_identification": True,
                })
        
        return committee
    
    def _infer_role(self, title: str) -> str:
        """Infer buying committee role from job title."""
        title_lower = title.lower()
        
        if any(x in title_lower for x in ["cfo", "finance", "budget"]):
            return "Economic Buyer"
        elif any(x in title_lower for x in ["cto", "engineer", "technical", "developer"]):
            return "Technical Buyer"
        elif any(x in title_lower for x in ["ceo", "founder", "owner", "president"]):
            return "Decision Maker"
        elif any(x in title_lower for x in ["security", "compliance", "legal"]):
            return "Blocker"
        elif any(x in title_lower for x in ["manager", "director", "head"]):
            return "User Buyer"
        else:
            return "Champion"
    
    def _identify_pain_points(self, lead: Dict) -> List[Dict[str, Any]]:
        """Identify likely pain points based on industry."""
        industry = lead.get("industry", "technology").lower()
        
        # Get industry-specific pain points
        industry_pains = self.industry_pain_points.get(
            industry, 
            self.industry_pain_points["technology"]
        )
        
        # Add any explicitly mentioned pain points
        mentioned = lead.get("pain_points", [])
        
        pain_points = []
        
        # Add mentioned pain points with high confidence
        for pain in mentioned:
            pain_points.append({
                "pain_point": pain,
                "confidence": "high",
                "source": "mentioned",
            })
        
        # Add inferred pain points
        for pain in industry_pains[:3]:
            if pain not in mentioned:
                pain_points.append({
                    "pain_point": pain,
                    "confidence": "medium",
                    "source": "inferred_from_industry",
                })
        
        return pain_points
    
    def _identify_triggers(self, lead: Dict) -> List[Dict[str, Any]]:
        """Identify buying trigger events (simulated)."""
        triggers = []
        
        # Simulated trigger events
        company = lead.get("company", "")
        
        if lead.get("funding_raised"):
            triggers.append({
                "trigger": f"{company} raised funding",
                "type": "funding",
                "urgency": "high",
                "talking_point": "Congratulations on the recent funding! How are you planning to scale?",
            })
        
        if lead.get("hiring"):
            triggers.append({
                "trigger": f"{company} is hiring aggressively",
                "type": "growth",
                "urgency": "medium",
                "talking_point": "I noticed you're scaling the team. How are you handling the increased complexity?",
            })
        
        if lead.get("new_executive"):
            triggers.append({
                "trigger": f"New executive joined {company}",
                "type": "leadership_change",
                "urgency": "high",
                "talking_point": "New leaders often bring fresh perspectives. What's on your priority list?",
            })
        
        # Default trigger if none found
        if not triggers:
            triggers.append({
                "trigger": "General outreach",
                "type": "cold",
                "urgency": "low",
                "talking_point": "I've been researching companies in your space...",
            })
        
        return triggers
    
    def _generate_personalization_hooks(
        self,
        profile: Dict,
        pain_points: List[Dict],
        triggers: List[Dict]
    ) -> List[str]:
        """Generate personalization hooks for outreach."""
        hooks = []
        
        # Company-based hook
        if profile.get("tier") == "enterprise":
            hooks.append(f"As a leader in {profile.get('industry', 'your industry')}, you likely face...")
        else:
            hooks.append(f"Fast-growing companies like {profile.get('name')} often struggle with...")
        
        # Pain point hook
        if pain_points:
            pain = pain_points[0]["pain_point"]
            hooks.append(f"Many {profile.get('industry', '')} companies tell us {pain} is a top challenge...")
        
        # Trigger hook
        if triggers and triggers[0]["type"] != "cold":
            hooks.append(triggers[0]["talking_point"])
        
        return hooks
