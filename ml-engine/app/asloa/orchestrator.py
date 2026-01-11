"""
ASLOA Orchestrator
Coordinates all 7 agents in the sales automation pipeline.

Pipeline Flow:
Lead → Score → Qualify → Research → Outreach → Route → CRM → Analytics
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
import logging

from app.asloa.agents.lead_scoring_agent import LeadScoringAgent
from app.asloa.agents.qualification_agent import QualificationAgent
from app.asloa.agents.research_agent import ResearchAgent
from app.asloa.agents.outreach_agent import OutreachAgent
from app.asloa.agents.routing_agent import RoutingAgent
from app.asloa.agents.crm_sync_agent import CRMSyncAgent
from app.asloa.agents.analytics_agent import AnalyticsAgent


class ASLOAOrchestrator:
    """
    ASLOA Pipeline Orchestrator
    
    Runs the complete sales automation pipeline:
    1. Lead Scoring - Score 0-100 based on ICP
    2. Qualification - BANT analysis
    3. Research - Company & contact intelligence
    4. Outreach - Personalized email generation
    5. Routing - Assign to best-fit rep
    6. CRM Sync - Update CRM records
    7. Analytics - Track metrics & forecast
    """
    
    def __init__(self):
        self.logger = logging.getLogger("asloa.orchestrator")
        
        # Initialize all agents
        self.lead_scoring = LeadScoringAgent()
        self.qualification = QualificationAgent()
        self.research = ResearchAgent()
        self.outreach = OutreachAgent()
        self.routing = RoutingAgent()
        self.crm_sync = CRMSyncAgent()
        self.analytics = AnalyticsAgent()
        
        # Pipeline config
        self.min_score_for_outreach = 40
        self.auto_send_threshold = 80  # Auto-send for hot leads
    
    def process_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a lead through the complete ASLOA pipeline.
        
        Input:
        - company: Company name
        - company_size: Employee count
        - industry: Industry vertical
        - contact_name: Contact name
        - contact_title: Job title
        - contact_email: Email address
        - source: Lead source
        - budget: Budget if known
        - pain_points: List of pain points
        - timeline: Buying timeline
        
        Returns complete pipeline result.
        """
        start_time = datetime.now()
        pipeline_id = f"asloa-{uuid.uuid4().hex[:12]}"
        lead_id = lead_data.get("lead_id", f"lead-{uuid.uuid4().hex[:8]}")
        
        self.logger.info(f"Starting ASLOA pipeline {pipeline_id} for lead {lead_id}")
        
        errors: List[str] = []
        
        try:
            # ============================================
            # Step 1: Lead Scoring
            # ============================================
            scoring_result = self.lead_scoring.process({
                "lead_id": lead_id,
                **lead_data
            })
            
            if scoring_result["status"] != "success":
                errors.append(f"Scoring: {scoring_result.get('error', 'unknown')}")
            
            score = scoring_result.get("scoring", {}).get("score", 50)
            tier = scoring_result.get("scoring", {}).get("tier", "COLD")
            
            # ============================================
            # Step 2: Qualification (BANT)
            # ============================================
            qualification_result = self.qualification.process({
                "lead_id": lead_id,
                "budget": lead_data.get("budget", 0),
                "budget_confirmed": lead_data.get("budget_confirmed", False),
                "contact_title": lead_data.get("contact_title", ""),
                "is_decision_maker": lead_data.get("is_decision_maker"),
                "pain_points": lead_data.get("pain_points", []),
                "needs_description": lead_data.get("needs_description", ""),
                "timeline": lead_data.get("timeline"),
                "urgency_signals": lead_data.get("urgency_signals", []),
            })
            
            if qualification_result["status"] != "success":
                errors.append(f"Qualification: {qualification_result.get('error', 'unknown')}")
            
            qualification = qualification_result.get("qualification", {})
            
            # ============================================
            # Step 3: Research
            # ============================================
            research_result = self.research.process({
                "company": lead_data.get("company", ""),
                "domain": lead_data.get("domain", ""),
                "industry": lead_data.get("industry", "technology"),
                "company_size": lead_data.get("company_size", 100),
                "contact_name": lead_data.get("contact_name", ""),
                "contact_title": lead_data.get("contact_title", ""),
                "funding_raised": lead_data.get("funding_raised", False),
                "hiring": lead_data.get("hiring", False),
                "pain_points": lead_data.get("pain_points", []),
            })
            
            if research_result["status"] != "success":
                errors.append(f"Research: {research_result.get('error', 'unknown')}")
            
            research = research_result.get("research", {})
            
            # ============================================
            # Step 4: Outreach (if score above threshold)
            # ============================================
            outreach = None
            if score >= self.min_score_for_outreach:
                outreach_result = self.outreach.process({
                    "lead_id": lead_id,
                    "lead_tier": tier,
                    "company": lead_data.get("company", ""),
                    "contact_name": lead_data.get("contact_name", ""),
                    "contact_email": lead_data.get("contact_email", ""),
                    "industry": lead_data.get("industry", "technology"),
                    "pain_points": research.get("pain_points", []),
                    "triggers": research.get("triggers", []),
                    "personalization_hooks": research.get("personalization_hooks", []),
                })
                
                if outreach_result["status"] != "success":
                    errors.append(f"Outreach: {outreach_result.get('error', 'unknown')}")
                
                outreach = outreach_result.get("outreach", {})
            
            # ============================================
            # Step 5: Routing
            # ============================================
            routing_result = self.routing.process({
                "lead_id": lead_id,
                "company": lead_data.get("company", ""),
                "company_size": lead_data.get("company_size", 100),
                "industry": lead_data.get("industry", "technology"),
                "territory": lead_data.get("territory", ""),
                "deal_size_estimate": lead_data.get("deal_size_estimate", 50000),
                "lead_tier": tier,
                "lead_score": score,
            })
            
            if routing_result["status"] != "success":
                errors.append(f"Routing: {routing_result.get('error', 'unknown')}")
            
            routing = routing_result.get("routing", {})
            
            # ============================================
            # Step 6: CRM Sync
            # ============================================
            crm_result = self.crm_sync.process({
                "lead_id": lead_id,
                "company": lead_data.get("company", ""),
                "contact_name": lead_data.get("contact_name", ""),
                "contact_email": lead_data.get("contact_email", ""),
                "contact_title": lead_data.get("contact_title", ""),
                "score": score,
                "lead_tier": tier,
                "qualification": qualification,
                "routing": routing,
                "outreach": outreach,
                "industry": lead_data.get("industry", ""),
                "company_size": lead_data.get("company_size", 0),
                "deal_size_estimate": lead_data.get("deal_size_estimate", 0),
                "source": lead_data.get("source", ""),
            })
            
            if crm_result["status"] != "success":
                errors.append(f"CRM: {crm_result.get('error', 'unknown')}")
            
            crm_sync = crm_result.get("crm_sync", {})
            
            # ============================================
            # Step 7: Analytics
            # ============================================
            analytics_result = self.analytics.process({
                "lead_id": lead_id,
                "score": score,
                "lead_tier": tier,
                "qualification": qualification,
                "deal_size_estimate": lead_data.get("deal_size_estimate", 50000),
                "routing": routing,
            })
            
            if analytics_result["status"] != "success":
                errors.append(f"Analytics: {analytics_result.get('error', 'unknown')}")
            
            analytics = analytics_result.get("analytics", {})
            
            # ============================================
            # Build final output
            # ============================================
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            result = {
                "pipeline_id": pipeline_id,
                "lead_id": lead_id,
                "status": "completed" if not errors else "completed_with_errors",
                "processing_time_ms": processing_time,
                
                # Pipeline results
                "scoring": scoring_result.get("scoring", {}),
                "qualification": qualification,
                "research": research,
                "outreach": outreach,
                "routing": routing,
                "crm_sync": crm_sync,
                "analytics": analytics,
                
                # Summary
                "summary": self._generate_summary(
                    lead_id, lead_data, score, tier, 
                    qualification, routing, outreach, analytics
                ),
                
                # Actions taken
                "actions_taken": self._list_actions(crm_sync, outreach, routing),
                
                "errors": errors,
                "timestamp": datetime.now().isoformat(),
            }
            
            self.logger.info(f"Pipeline {pipeline_id} completed in {processing_time:.0f}ms")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            return {
                "pipeline_id": pipeline_id,
                "lead_id": lead_id,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }
    
    def _generate_summary(
        self, lead_id: str, lead_data: Dict, score: int, tier: str,
        qualification: Dict, routing: Dict, outreach: Dict, analytics: Dict
    ) -> Dict[str, Any]:
        """Generate human-readable summary."""
        company = lead_data.get("company", "Company")
        contact = lead_data.get("contact_name", "Contact")
        qual_status = qualification.get("qualification_status", "UNKNOWN")
        assigned_to = routing.get("assigned_to", {}).get("name", "Unassigned")
        
        headline = f"Lead {company} processed: {tier} ({score}/100)"
        
        actions = []
        if score >= 60:
            actions.append(f"Scored as {tier} lead")
        if qual_status in ["QUALIFIED", "PARTIALLY_QUALIFIED"]:
            actions.append(f"BANT: {qual_status}")
        if outreach:
            actions.append("Personalized email drafted")
        if routing:
            actions.append(f"Assigned to {assigned_to}")
        
        # Time saved
        time_saved = analytics.get("time_saved", {}).get("this_lead_minutes", 105)
        
        return {
            "headline": headline,
            "lead": {
                "company": company,
                "contact": contact,
                "score": score,
                "tier": tier,
                "status": qual_status,
            },
            "actions_summary": " | ".join(actions),
            "assigned_to": assigned_to,
            "time_saved_minutes": time_saved,
            "next_step": routing.get("expected_response_time", "Within 24 hours"),
            "message_for_ui": f"{tier} lead from {company} scored {score}/100 and assigned to {assigned_to}. {time_saved} minutes of work automated by ASLOA.",
        }
    
    def _list_actions(
        self, crm_sync: Dict, outreach: Dict, routing: Dict
    ) -> List[Dict[str, Any]]:
        """List all actions taken by the pipeline."""
        actions = []
        
        # Scoring action
        actions.append({
            "action": "LEAD_SCORED",
            "status": "completed",
            "details": "ICP scoring completed",
        })
        
        # Qualification action
        actions.append({
            "action": "BANT_QUALIFIED",
            "status": "completed",
            "details": "BANT qualification completed",
        })
        
        # Research action
        actions.append({
            "action": "PROSPECT_RESEARCHED",
            "status": "completed",
            "details": "Company & contact research completed",
        })
        
        # Outreach action
        if outreach:
            actions.append({
                "action": "EMAIL_DRAFTED",
                "status": "completed",
                "details": f"Personalized email created using {outreach.get('email', {}).get('template_used', 'template')}",
            })
        
        # Routing action
        if routing and routing.get("assigned_to"):
            actions.append({
                "action": "LEAD_ROUTED",
                "status": "completed",
                "details": f"Assigned to {routing['assigned_to'].get('name', 'rep')}",
            })
        
        # CRM actions
        if crm_sync:
            if crm_sync.get("crm_record"):
                actions.append({
                    "action": "CRM_RECORD_CREATED",
                    "status": "completed",
                    "details": "Lead record created in CRM",
                })
            
            if crm_sync.get("tasks_created"):
                actions.append({
                    "action": "TASKS_CREATED",
                    "status": "completed",
                    "details": f"{len(crm_sync['tasks_created'])} follow-up tasks created",
                })
            
            if crm_sync.get("notifications_sent"):
                actions.append({
                    "action": "NOTIFICATIONS_SENT",
                    "status": "completed",
                    "details": f"{len(crm_sync['notifications_sent'])} notifications sent",
                })
        
        return actions
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get dashboard data from analytics agent."""
        return self.analytics.get_dashboard_data()
