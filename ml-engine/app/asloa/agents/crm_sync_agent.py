"""
ASLOA - CRM Sync Agent
Automatic CRM record management.

Capabilities:
- Create/update lead records
- Auto-task creation
- Activity logging
- Pipeline updates
- Notification triggers
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import uuid

from app.agents.base_agent import BaseAgent


class CRMSyncAgent(BaseAgent):
    """
    CRM Sync Agent - Manages all CRM operations.
    
    Integrates with CRM systems (HubSpot, Salesforce, Zoho, etc.)
    to automatically create and update records.
    """
    
    def __init__(self):
        super().__init__("crm_sync")
        
        # Simulated CRM (in production, this would be API calls)
        self.crm_records: Dict[str, Any] = {}
        self.tasks: List[Dict] = []
        self.activities: List[Dict] = []
        self.notifications: List[Dict] = []
    
    def process(
        self,
        input_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Sync lead data to CRM.
        
        Input:
        - lead_id: Lead identifier
        - company: Company name
        - contact_name: Contact name
        - contact_email: Email
        - contact_phone: Phone (optional)
        - score: Lead score
        - qualification: Qualification result
        - routing: Routing assignment
        - outreach: Outreach details
        - stage: Pipeline stage
        """
        start_time = self._start_processing()
        
        try:
            lead_id = input_data.get("lead_id", f"lead-{uuid.uuid4().hex[:8]}")
            
            # Create or update lead record
            lead_record = self._create_or_update_lead(lead_id, input_data)
            
            # Create tasks for assigned rep
            tasks_created = self._create_tasks(lead_id, input_data)
            
            # Log activities
            activities_logged = self._log_activities(lead_id, input_data)
            
            # Send notifications
            notifications_sent = self._send_notifications(lead_id, input_data)
            
            # Update pipeline
            pipeline_update = self._update_pipeline(lead_id, input_data)
            
            result = {
                "lead_id": lead_id,
                "crm_record": lead_record,
                "tasks_created": tasks_created,
                "activities_logged": activities_logged,
                "notifications_sent": notifications_sent,
                "pipeline_update": pipeline_update,
                "sync_status": "success",
                "synced_at": datetime.now().isoformat(),
            }
            
            self._complete_processing(start_time, success=True)
            self._last_output = result
            
            return {
                "status": "success",
                "crm_sync": result,
            }
            
        except Exception as e:
            self._log_error(e, "CRM sync failed")
            self._complete_processing(start_time, success=False)
            return {"status": "error", "error": str(e)}
    
    def _create_or_update_lead(self, lead_id: str, data: Dict) -> Dict[str, Any]:
        """Create or update lead record in CRM."""
        # Check if exists
        is_update = lead_id in self.crm_records
        
        # Build record
        record = {
            "id": lead_id,
            "type": "lead",
            "company": data.get("company", ""),
            "contact": {
                "name": data.get("contact_name", ""),
                "email": data.get("contact_email", ""),
                "phone": data.get("contact_phone", ""),
                "title": data.get("contact_title", ""),
            },
            "score": data.get("score", 0),
            "tier": data.get("lead_tier", "COLD"),
            "qualification_status": data.get("qualification", {}).get("qualification_status", "PENDING"),
            "assigned_to": data.get("routing", {}).get("assigned_to", {}),
            "stage": data.get("stage", "new"),
            "source": data.get("source", "website"),
            "industry": data.get("industry", ""),
            "company_size": data.get("company_size", 0),
            "deal_value": data.get("deal_size_estimate", 0),
            "created_at": self.crm_records.get(lead_id, {}).get("created_at", datetime.now().isoformat()),
            "updated_at": datetime.now().isoformat(),
            "asloa_processed": True,
        }
        
        # Store
        self.crm_records[lead_id] = record
        
        return {
            "record_id": lead_id,
            "action": "updated" if is_update else "created",
            "record": record,
        }
    
    def _create_tasks(self, lead_id: str, data: Dict) -> List[Dict[str, Any]]:
        """Create follow-up tasks for assigned rep."""
        tasks = []
        routing = data.get("routing", {})
        assigned_to = routing.get("assigned_to", {})
        lead_tier = data.get("lead_tier", "COLD")
        
        if not assigned_to:
            return tasks
        
        # Task 1: Initial outreach
        if lead_tier == "HOT":
            due_time = timedelta(minutes=5)
            priority = "urgent"
        elif lead_tier == "WARM":
            due_time = timedelta(hours=2)
            priority = "high"
        else:
            due_time = timedelta(hours=24)
            priority = "normal"
        
        task1 = {
            "task_id": f"task-{uuid.uuid4().hex[:8]}",
            "type": "outreach",
            "title": f"Reach out to {data.get('contact_name', 'lead')} at {data.get('company', 'company')}",
            "description": f"Lead score: {data.get('score', 0)}. See ASLOA research for personalization.",
            "assigned_to": assigned_to.get("rep_id", ""),
            "lead_id": lead_id,
            "due_at": (datetime.now() + due_time).isoformat(),
            "priority": priority,
            "status": "pending",
        }
        tasks.append(task1)
        self.tasks.append(task1)
        
        # Task 2: Follow-up if no response
        task2 = {
            "task_id": f"task-{uuid.uuid4().hex[:8]}",
            "type": "follow_up",
            "title": f"Follow up with {data.get('contact_name', 'lead')} if no response",
            "assigned_to": assigned_to.get("rep_id", ""),
            "lead_id": lead_id,
            "due_at": (datetime.now() + timedelta(days=3)).isoformat(),
            "priority": "normal",
            "status": "pending",
            "depends_on": task1["task_id"],
        }
        tasks.append(task2)
        self.tasks.append(task2)
        
        return tasks
    
    def _log_activities(self, lead_id: str, data: Dict) -> List[Dict[str, Any]]:
        """Log activities in CRM."""
        activities = []
        
        # Activity: Lead scored
        if data.get("score"):
            activity = {
                "activity_id": f"act-{uuid.uuid4().hex[:8]}",
                "type": "lead_scored",
                "lead_id": lead_id,
                "description": f"ASLOA scored lead at {data.get('score', 0)}/100 ({data.get('lead_tier', 'COLD')})",
                "automated": True,
                "timestamp": datetime.now().isoformat(),
            }
            activities.append(activity)
            self.activities.append(activity)
        
        # Activity: Lead qualified
        if data.get("qualification"):
            qual = data["qualification"]
            activity = {
                "activity_id": f"act-{uuid.uuid4().hex[:8]}",
                "type": "lead_qualified",
                "lead_id": lead_id,
                "description": f"BANT qualification: {qual.get('qualification_status', 'UNKNOWN')}",
                "automated": True,
                "timestamp": datetime.now().isoformat(),
            }
            activities.append(activity)
            self.activities.append(activity)
        
        # Activity: Lead routed
        if data.get("routing"):
            routing = data["routing"]
            activity = {
                "activity_id": f"act-{uuid.uuid4().hex[:8]}",
                "type": "lead_routed",
                "lead_id": lead_id,
                "description": f"Assigned to {routing.get('assigned_to', {}).get('name', 'rep')}",
                "automated": True,
                "timestamp": datetime.now().isoformat(),
            }
            activities.append(activity)
            self.activities.append(activity)
        
        # Activity: Outreach sent
        if data.get("outreach"):
            activity = {
                "activity_id": f"act-{uuid.uuid4().hex[:8]}",
                "type": "email_drafted",
                "lead_id": lead_id,
                "description": "ASLOA generated personalized outreach email",
                "automated": True,
                "timestamp": datetime.now().isoformat(),
            }
            activities.append(activity)
            self.activities.append(activity)
        
        return activities
    
    def _send_notifications(self, lead_id: str, data: Dict) -> List[Dict[str, Any]]:
        """Send notifications to relevant parties."""
        notifications = []
        routing = data.get("routing", {})
        assigned_to = routing.get("assigned_to", {})
        lead_tier = data.get("lead_tier", "COLD")
        
        if assigned_to:
            # Notify assigned rep
            notif = {
                "notification_id": f"notif-{uuid.uuid4().hex[:8]}",
                "type": "new_lead_assigned",
                "recipient": assigned_to.get("email", ""),
                "title": f"New {lead_tier} Lead Assigned: {data.get('company', 'Company')}",
                "body": f"Lead Score: {data.get('score', 0)}/100. Contact: {data.get('contact_name', 'N/A')}",
                "lead_id": lead_id,
                "priority": "high" if lead_tier == "HOT" else "normal",
                "sent_at": datetime.now().isoformat(),
            }
            notifications.append(notif)
            self.notifications.append(notif)
            
            # Notify manager for hot leads
            if lead_tier == "HOT" and data.get("deal_size_estimate", 0) > 50000:
                notif_mgr = {
                    "notification_id": f"notif-{uuid.uuid4().hex[:8]}",
                    "type": "hot_lead_alert",
                    "recipient": "sales-manager@company.com",
                    "title": f"HOT Lead Alert: {data.get('company', 'Company')} (${data.get('deal_size_estimate', 0):,})",
                    "body": f"High-value lead assigned to {assigned_to.get('name', 'rep')}",
                    "lead_id": lead_id,
                    "priority": "urgent",
                    "sent_at": datetime.now().isoformat(),
                }
                notifications.append(notif_mgr)
                self.notifications.append(notif_mgr)
        
        return notifications
    
    def _update_pipeline(self, lead_id: str, data: Dict) -> Dict[str, Any]:
        """Update pipeline stage and metrics."""
        qualification = data.get("qualification", {})
        qual_status = qualification.get("qualification_status", "PENDING")
        
        # Determine stage
        if qual_status == "QUALIFIED":
            stage = "qualified"
            probability = 0.25
        elif qual_status == "PARTIALLY_QUALIFIED":
            stage = "discovery"
            probability = 0.15
        else:
            stage = "new"
            probability = 0.05
        
        return {
            "lead_id": lead_id,
            "stage": stage,
            "probability": probability,
            "deal_value": data.get("deal_size_estimate", 0),
            "weighted_value": data.get("deal_size_estimate", 0) * probability,
            "updated_at": datetime.now().isoformat(),
        }
