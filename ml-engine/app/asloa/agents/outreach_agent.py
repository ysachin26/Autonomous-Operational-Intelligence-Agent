"""
ASLOA - Outreach Agent
Generates personalized sales emails based on research.

Capabilities:
- Industry-specific templates
- Role-based messaging
- Pain point addressing
- Buying trigger incorporation
- A/B variant generation
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
import random

from app.agents.base_agent import BaseAgent


class OutreachAgent(BaseAgent):
    """
    Outreach Agent - Generates personalized sales emails.
    
    Creates context-aware, personalized outreach based on:
    - Prospect's industry and company size
    - Contact's role and seniority
    - Identified pain points
    - Buying triggers
    """
    
    def __init__(self):
        super().__init__("outreach")
        
        # Email templates by scenario
        self.templates = {
            "hot_lead": {
                "subject": "Quick question about {pain_point} at {company}",
                "body": """Hi {first_name},

{personalization_hook}

I noticed {trigger_context}. Many {industry} leaders we work with face similar challenges around {pain_point}.

We've helped companies like {reference_company} achieve {result} in just {timeframe}.

Would you be open to a 15-minute call this week to explore if we could help {company} achieve similar results?

Best,
{sender_name}""",
            },
            "warm_lead": {
                "subject": "Idea for {company}'s {pain_point} challenge",
                "body": """Hi {first_name},

{personalization_hook}

I've been researching {company} and came across {trigger_context}. 

Based on what I'm seeing in the {industry} space, I believe there might be an opportunity to {value_prop}.

I'd love to share a few quick insights. Would you be open to a brief conversation?

Best,
{sender_name}""",
            },
            "cold_lead": {
                "subject": "{first_name}, quick question",
                "body": """Hi {first_name},

I'm reaching out because we help {industry} companies like {company} with {pain_point}.

Our customers typically see {result} within {timeframe} of working with us.

If this is a priority for you right now, I'd love to share how we might help.

Would a quick 10-minute call work for you?

Best,
{sender_name}""",
            },
            "follow_up": {
                "subject": "Re: {original_subject}",
                "body": """Hi {first_name},

Just following up on my previous note. I know you're busy, so I'll keep this brief.

{follow_up_hook}

If now isn't the right time, no worries at all. But if {pain_point} is on your radar, I'd welcome the chance to share what's working for similar companies.

Best,
{sender_name}""",
            },
        }
        
        # Result templates by industry
        self.results = {
            "technology": ["40% faster deployment", "3x developer productivity", "50% reduction in incidents"],
            "saas": ["25% reduction in churn", "2x user activation", "40% more expansion revenue"],
            "manufacturing": ["30% less downtime", "25% productivity increase", "15% cost reduction"],
            "retail": ["20% inventory efficiency", "35% faster fulfillment", "15% labor cost savings"],
            "healthcare": ["40% shorter wait times", "25% better staff utilization", "30% compliance improvement"],
        }
    
    def process(
        self,
        input_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate personalized outreach email.
        
        Input:
        - lead_id: Lead identifier
        - lead_tier: HOT, WARM, or COLD
        - company: Company name
        - contact_name: Full name
        - contact_email: Email address
        - industry: Industry vertical
        - pain_points: List of pain points
        - triggers: List of trigger events
        - personalization_hooks: Hooks from research
        - is_follow_up: Whether this is a follow-up
        """
        start_time = self._start_processing()
        
        try:
            lead_id = input_data.get("lead_id", f"lead-{uuid.uuid4().hex[:8]}")
            
            # Determine template to use
            template_key = self._select_template(input_data)
            template = self.templates[template_key]
            
            # Get first name
            full_name = input_data.get("contact_name", "there")
            first_name = full_name.split()[0] if full_name else "there"
            
            # Prepare personalization data
            industry = input_data.get("industry", "technology").lower()
            pain_points = input_data.get("pain_points", [])
            triggers = input_data.get("triggers", [])
            hooks = input_data.get("personalization_hooks", [])
            
            # Select components
            pain_point = pain_points[0]["pain_point"] if pain_points else "operational efficiency"
            trigger_context = triggers[0]["talking_point"] if triggers else "your company's growth"
            personalization_hook = hooks[0] if hooks else f"I've been following {input_data.get('company', 'your company')}'s journey."
            
            # Get result for industry
            results = self.results.get(industry, self.results["technology"])
            result = random.choice(results)
            
            # Fill template
            email_data = {
                "first_name": first_name,
                "company": input_data.get("company", "your company"),
                "industry": industry,
                "pain_point": pain_point,
                "trigger_context": trigger_context,
                "personalization_hook": personalization_hook,
                "result": result,
                "timeframe": "90 days",
                "reference_company": f"similar {industry} companies",
                "value_prop": f"improve {pain_point}",
                "sender_name": "ASLOA Sales Team",
                "follow_up_hook": "I wanted to make sure this didn't get buried in your inbox.",
                "original_subject": f"Quick question about {pain_point}",
            }
            
            subject = template["subject"].format(**email_data)
            body = template["body"].format(**email_data)
            
            # Generate A/B variant
            variant_subject = self._generate_variant_subject(
                subject, first_name, input_data.get("company", "")
            )
            
            result = {
                "lead_id": lead_id,
                "email": {
                    "to": input_data.get("contact_email", ""),
                    "subject": subject,
                    "body": body,
                    "template_used": template_key,
                },
                "variant": {
                    "subject": variant_subject,
                    "body": body,  # Same body, different subject for A/B
                },
                "personalization_score": self._calculate_personalization_score(input_data),
                "send_recommendation": self._get_send_recommendation(input_data),
                "generated_at": datetime.now().isoformat(),
            }
            
            self._complete_processing(start_time, success=True)
            self._last_output = result
            
            return {
                "status": "success",
                "outreach": result,
            }
            
        except Exception as e:
            self._log_error(e, "Outreach generation failed")
            self._complete_processing(start_time, success=False)
            return {"status": "error", "error": str(e)}
    
    def _select_template(self, lead: Dict) -> str:
        """Select appropriate template based on lead data."""
        if lead.get("is_follow_up"):
            return "follow_up"
        
        tier = lead.get("lead_tier", "COLD").upper()
        
        if tier == "HOT":
            return "hot_lead"
        elif tier == "WARM":
            return "warm_lead"
        else:
            return "cold_lead"
    
    def _generate_variant_subject(
        self, original: str, first_name: str, company: str
    ) -> str:
        """Generate A/B variant subject line."""
        variants = [
            f"{first_name} - thought you'd find this interesting",
            f"Idea for {company}",
            f"{first_name}, are you thinking about this?",
            f"Can I share a quick insight, {first_name}?",
        ]
        return random.choice(variants)
    
    def _calculate_personalization_score(self, lead: Dict) -> int:
        """Calculate how personalized the email is (0-100)."""
        score = 50  # Base score
        
        if lead.get("pain_points"):
            score += 15
        if lead.get("triggers"):
            score += 15
        if lead.get("personalization_hooks"):
            score += 10
        if lead.get("industry"):
            score += 5
        if lead.get("contact_name"):
            score += 5
        
        return min(score, 100)
    
    def _get_send_recommendation(self, lead: Dict) -> Dict[str, Any]:
        """Get recommendation for when to send."""
        tier = lead.get("lead_tier", "COLD").upper()
        
        # Best send times (simulated)
        if tier == "HOT":
            return {
                "urgency": "immediate",
                "best_time": "ASAP",
                "reason": "Hot lead - respond within 5 minutes for best conversion",
            }
        elif tier == "WARM":
            return {
                "urgency": "within_24h",
                "best_time": "Tuesday-Thursday, 9-11 AM",
                "reason": "Warm lead - personalized outreach yields best results",
            }
        else:
            return {
                "urgency": "within_week",
                "best_time": "Tuesday 10 AM or Wednesday 2 PM",
                "reason": "Cold outreach - timing matters for open rates",
            }
