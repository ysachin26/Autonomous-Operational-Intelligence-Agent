"""
ASLOA API Endpoints
Sales automation pipeline API.
"""

from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime

from app.asloa.orchestrator import ASLOAOrchestrator


router = APIRouter(prefix="/asloa", tags=["ASLOA Sales Automation"])


# Request/Response Models
class LeadInput(BaseModel):
    """Lead input for processing."""
    company: str = Field(..., description="Company name")
    company_size: Optional[int] = Field(100, description="Employee count")
    industry: Optional[str] = Field("technology", description="Industry vertical")
    
    contact_name: str = Field(..., description="Contact name")
    contact_title: Optional[str] = Field("", description="Job title")
    contact_email: str = Field(..., description="Email address")
    
    source: Optional[str] = Field("website", description="Lead source")
    budget: Optional[float] = Field(0, description="Budget if known")
    budget_confirmed: Optional[bool] = Field(False)
    
    deal_size_estimate: Optional[float] = Field(50000, description="Estimated deal value")
    
    pain_points: Optional[List[str]] = Field(default_factory=list)
    needs_description: Optional[str] = Field("")
    timeline: Optional[int] = Field(None, description="Buying timeline in days")
    urgency_signals: Optional[List[str]] = Field(default_factory=list)
    
    territory: Optional[str] = Field("", description="Geographic region")
    funding_raised: Optional[bool] = Field(False)
    hiring: Optional[bool] = Field(False)
    
    class Config:
        json_schema_extra = {
            "example": {
                "company": "TechCorp Inc",
                "company_size": 250,
                "industry": "saas",
                "contact_name": "John Smith",
                "contact_title": "VP of Engineering",
                "contact_email": "john@techcorp.com",
                "source": "linkedin",
                "budget": 75000,
                "deal_size_estimate": 100000,
                "pain_points": ["Developer productivity", "Deployment speed"],
                "timeline": 60,
            }
        }


class LeadProcessResponse(BaseModel):
    """Response from lead processing."""
    pipeline_id: str
    lead_id: str
    status: str
    processing_time_ms: float
    
    scoring: Dict[str, Any]
    qualification: Dict[str, Any]
    research: Dict[str, Any]
    outreach: Optional[Dict[str, Any]]
    routing: Dict[str, Any]
    crm_sync: Dict[str, Any]
    analytics: Dict[str, Any]
    
    summary: Dict[str, Any]
    actions_taken: List[Dict[str, Any]]
    
    errors: List[str]
    timestamp: str


# Orchestrator instance
orchestrator = ASLOAOrchestrator()


@router.post("/process-lead", response_model=LeadProcessResponse)
async def process_lead(lead: LeadInput) -> LeadProcessResponse:
    """
    Process a lead through the complete ASLOA pipeline.
    
    Pipeline steps:
    1. Lead Scoring (0-100 ICP score)
    2. BANT Qualification
    3. Prospect Research
    4. Personalized Outreach
    5. Rep Assignment
    6. CRM Sync
    7. Analytics
    
    Returns complete processing result with all actions taken.
    """
    try:
        result = orchestrator.process_lead(lead.model_dump())
        return LeadProcessResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard")
async def get_dashboard() -> Dict[str, Any]:
    """
    Get ASLOA dashboard data.
    
    Returns:
    - Pipeline metrics
    - Conversion rates
    - Time saved
    - Rep performance
    """
    return orchestrator.get_dashboard_data()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """ASLOA health check."""
    return {
        "status": "healthy",
        "service": "ASLOA",
        "agents": {
            "lead_scoring": "active",
            "qualification": "active",
            "research": "active",
            "outreach": "active",
            "routing": "active",
            "crm_sync": "active",
            "analytics": "active",
        },
        "timestamp": datetime.now().isoformat(),
    }
