"""
ASLOA Demo - Sales Lead Automation Demonstration
Complete end-to-end demo for hackathon judges.
"""

from datetime import datetime
import json

from app.asloa.orchestrator import ASLOAOrchestrator


def run_asloa_demo():
    """Run complete ASLOA sales automation demo."""
    
    print("\n" + "=" * 70)
    print("ASLOA - AI SALES LEAD OPERATIONS AGENT")
    print("Integrated with AOIA for Autonomous Sales Pipeline")
    print("=" * 70)
    
    # Initialize
    orchestrator = ASLOAOrchestrator()
    
    # Demo lead data
    lead = {
        "company": "TechCorp Industries",
        "company_size": 350,
        "industry": "saas",
        "contact_name": "Priya Sharma",
        "contact_title": "VP of Engineering",
        "contact_email": "priya@techcorp.com",
        "source": "linkedin",
        "budget": 85000,
        "budget_confirmed": True,
        "deal_size_estimate": 120000,
        "pain_points": [
            "Developer productivity bottleneck",
            "Slow deployment cycles",
            "Technical debt accumulation"
        ],
        "needs_description": "Looking for automation tools to improve engineering velocity",
        "timeline": 45,  # 45 days
        "urgency_signals": ["Q1 budget available", "New CTO mandate"],
        "territory": "west",
        "funding_raised": True,
        "hiring": True,
    }
    
    print("\n" + "-" * 60)
    print("INCOMING LEAD")
    print("-" * 60)
    print(f"""
Company:    {lead['company']}
Contact:    {lead['contact_name']} ({lead['contact_title']})
Email:      {lead['contact_email']}
Size:       {lead['company_size']} employees
Industry:   {lead['industry']}
Budget:     ${lead['budget']:,} (CONFIRMED)
Timeline:   {lead['timeline']} days
Source:     {lead['source']}
""")
    
    print("-" * 60)
    print("RUNNING ASLOA PIPELINE...")
    print("-" * 60)
    
    # Process the lead
    result = orchestrator.process_lead(lead)
    
    # Display results
    print("\n" + "-" * 60)
    print("STEP 1: LEAD SCORING")
    print("-" * 60)
    scoring = result.get("scoring", {})
    print(f"""
Score:       {scoring.get('score', 0)}/100
Tier:        {scoring.get('tier', 'N/A')}
Priority:    {scoring.get('priority', 'N/A')}
Recommendation: {scoring.get('recommendation', 'N/A')}

Breakdown:
  Company Size:    {scoring.get('breakdown', {}).get('company_size_score', 0)}/20
  Industry:        {scoring.get('breakdown', {}).get('industry_score', 0)}/20
  Authority:       {scoring.get('breakdown', {}).get('authority_score', 0)}/20
  Engagement:      {scoring.get('breakdown', {}).get('engagement_score', 0)}/20
  Budget Signals:  {scoring.get('breakdown', {}).get('budget_signals_score', 0)}/20
""")
    
    print("-" * 60)
    print("STEP 2: BANT QUALIFICATION")
    print("-" * 60)
    qual = result.get("qualification", {})
    bant = qual.get("bant_analysis", {})
    print(f"""
Status:      {qual.get('qualification_status', 'N/A')}
Criteria:    {qual.get('qualified_criteria', 0)}/4 met
Confidence:  {qual.get('confidence', 0)*100:.0f}%

BANT Analysis:
  Budget:    {'QUALIFIED' if bant.get('budget', {}).get('qualified') else 'GAP'} - {bant.get('budget', {}).get('reason', '')}
  Authority: {'QUALIFIED' if bant.get('authority', {}).get('qualified') else 'GAP'} - {bant.get('authority', {}).get('reason', '')}
  Need:      {'QUALIFIED' if bant.get('need', {}).get('qualified') else 'GAP'} - {bant.get('need', {}).get('reason', '')}
  Timeline:  {'QUALIFIED' if bant.get('timeline', {}).get('qualified') else 'GAP'} - {bant.get('timeline', {}).get('reason', '')}
""")
    
    print("-" * 60)
    print("STEP 3: PROSPECT RESEARCH")
    print("-" * 60)
    research = result.get("research", {})
    profile = research.get("company_profile", {})
    print(f"""
Company Profile:
  Name:     {profile.get('name', 'N/A')}
  Tier:     {profile.get('tier', 'N/A')}
  Revenue:  {profile.get('revenue_estimate', 'N/A')}
  Size:     {profile.get('employee_count', 0)} employees

Buying Committee:""")
    for member in research.get("buying_committee", [])[:3]:
        print(f"  - {member.get('name', 'Unknown')}: {member.get('title', '')} ({member.get('role', '')})")
    
    print("\nIdentified Pain Points:")
    for pain in research.get("pain_points", [])[:3]:
        print(f"  - [{pain.get('confidence', 'N/A')}] {pain.get('pain_point', '')}")
    
    print("-" * 60)
    print("STEP 4: PERSONALIZED OUTREACH")
    print("-" * 60)
    outreach = result.get("outreach", {})
    if outreach:
        email = outreach.get("email", {})
        print(f"""
To:      {email.get('to', 'N/A')}
Subject: {email.get('subject', 'N/A')}

{email.get('body', 'N/A')}

Personalization Score: {outreach.get('personalization_score', 0)}/100
Send Recommendation: {outreach.get('send_recommendation', {}).get('best_time', 'ASAP')}
""")
    
    print("-" * 60)
    print("STEP 5: LEAD ROUTING")
    print("-" * 60)
    routing = result.get("routing", {})
    assigned = routing.get("assigned_to", {})
    print(f"""
Assigned To:    {assigned.get('name', 'N/A')}
Rep Email:      {assigned.get('email', 'N/A')}
Match Score:    {routing.get('assignment_score', 0)}/100
Reason:         {routing.get('reason', 'N/A')}
Expected Response: {routing.get('expected_response_time', 'N/A')}
""")
    
    print("-" * 60)
    print("STEP 6: CRM SYNC")
    print("-" * 60)
    crm = result.get("crm_sync", {})
    print(f"""
CRM Record:     {crm.get('crm_record', {}).get('action', 'N/A')}
Tasks Created:  {len(crm.get('tasks_created', []))}
Activities:     {len(crm.get('activities_logged', []))}
Notifications:  {len(crm.get('notifications_sent', []))}

Pipeline Stage: {crm.get('pipeline_update', {}).get('stage', 'N/A')}
Win Probability: {crm.get('pipeline_update', {}).get('probability', 0)*100:.0f}%
""")
    
    print("-" * 60)
    print("STEP 7: ANALYTICS")
    print("-" * 60)
    analytics = result.get("analytics", {})
    time_saved = analytics.get("time_saved", {})
    forecast = analytics.get("forecast_impact", {})
    print(f"""
Time Saved This Lead: {time_saved.get('this_lead_minutes', 0)} minutes
Value Saved:          ${time_saved.get('value_saved_usd', 0):,.0f}

Conversion Probability: {analytics.get('conversion_probability', {}).get('probability', 0)*100:.1f}%
Expected Revenue:       ${forecast.get('expected_revenue', 0):,.0f}
Forecast Month:         {forecast.get('forecast_month', 'N/A')}
""")
    
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    summary = result.get("summary", {})
    print(f"""
{summary.get('headline', '')}

{summary.get('message_for_ui', '')}

ACTIONS TAKEN:""")
    for action in result.get("actions_taken", []):
        print(f"  [{action.get('status', '').upper()}] {action.get('action', '')}")
    
    print(f"""
Processing Time: {result.get('processing_time_ms', 0):.0f}ms
Status: {result.get('status', 'N/A')}
""")
    
    print("=" * 70)
    print("ASLOA PIPELINE COMPLETE!")
    print("Lead -> Score -> Qualify -> Research -> Outreach -> Route -> CRM -> Analytics")
    print("=" * 70)
    
    return result


if __name__ == "__main__":
    run_asloa_demo()
