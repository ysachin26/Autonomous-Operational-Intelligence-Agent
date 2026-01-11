"""
ASLOA - AI Sales Lead Operations Agent
Autonomous sales pipeline integrated with AOIA.

7 Specialized Agents:
1. Lead Scoring Agent - ICP scoring 0-100
2. Qualification Agent - BANT analysis
3. Research Agent - Company/contact intelligence
4. Outreach Agent - Personalized email generation
5. Routing Agent - Smart rep assignment
6. CRM Sync Agent - Record management
7. Analytics Agent - Metrics & forecasting
"""

from app.asloa.agents.lead_scoring_agent import LeadScoringAgent
from app.asloa.agents.qualification_agent import QualificationAgent
from app.asloa.agents.research_agent import ResearchAgent
from app.asloa.agents.outreach_agent import OutreachAgent
from app.asloa.agents.routing_agent import RoutingAgent
from app.asloa.agents.crm_sync_agent import CRMSyncAgent
from app.asloa.agents.analytics_agent import AnalyticsAgent
from app.asloa.orchestrator import ASLOAOrchestrator

__all__ = [
    "LeadScoringAgent",
    "QualificationAgent",
    "ResearchAgent",
    "OutreachAgent",
    "RoutingAgent",
    "CRMSyncAgent",
    "AnalyticsAgent",
    "ASLOAOrchestrator",
]
