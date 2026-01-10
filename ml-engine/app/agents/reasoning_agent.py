"""
AOIA ML Engine - Reasoning Agent
AI-powered conversational agent for operational intelligence.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import re


class ReasoningAgent:
    """
    The AOIA Reasoning Agent handles natural language interactions,
    generates explanations, and provides intelligent responses about operations.
    
    In production, this would integrate with OpenAI GPT-4 or similar LLM.
    For demo purposes, uses intelligent template-based responses.
    """
    
    def __init__(self):
        self.conversation_history: Dict[str, List[Dict]] = {}
        
        # Intent patterns for query classification
        self.intent_patterns = {
            "status": r"(status|overview|how.*(doing|going)|current|state)",
            "anomaly": r"(anomal|issue|problem|wrong|error|alert)",
            "loss": r"(loss|cost|money|losing|financial|revenue)",
            "recommendation": r"(recommend|suggest|advice|optimize|improve|fix)",
            "explain": r"(explain|why|reason|cause|what happened)",
            "forecast": r"(predict|forecast|expect|future|next|will)",
            "compare": r"(compare|versus|vs|difference|between)",
            "help": r"(help|can you|what can|how do)",
        }
    
    def chat(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Process a chat message and generate a response.
        
        Args:
            message: User's message
            context: Operational context (anomalies, incidents, etc.)
            session_id: Session identifier for conversation continuity
        
        Returns:
            Response with message, intent, and suggested actions
        """
        session = session_id or f"session_{datetime.now().timestamp()}"
        
        # Classify intent
        intent = self._classify_intent(message)
        
        # Extract entities
        entities = self._extract_entities(message)
        
        # Generate response based on intent and context
        response = self._generate_response(intent, message, context or {}, entities)
        
        # Store in conversation history
        if session not in self.conversation_history:
            self.conversation_history[session] = []
        
        self.conversation_history[session].append({
            "role": "user",
            "content": message,
            "timestamp": self.get_timestamp(),
        })
        self.conversation_history[session].append({
            "role": "assistant",
            "content": response["message"],
            "timestamp": self.get_timestamp(),
        })
        
        return {
            "response": response["message"],
            "session_id": session,
            "intent": intent,
            "entities": entities,
            "suggested_actions": response.get("actions", []),
        }
    
    def explain(
        self,
        entity_type: str,
        entity: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate a detailed explanation for an anomaly or incident.
        
        Args:
            entity_type: "anomaly" or "incident"
            entity: The entity data to explain
            context: Additional context
        
        Returns:
            Detailed explanation with findings and recommendations
        """
        if entity_type == "anomaly":
            return self._explain_anomaly(entity, context)
        elif entity_type == "incident":
            return self._explain_incident(entity, context)
        else:
            return {
                "explanation": "Unable to generate explanation for unknown entity type.",
                "key_findings": [],
                "root_cause": None,
                "confidence": 0.0,
            }
    
    def summarize(
        self,
        data: Dict[str, Any],
        summary_type: str = "daily",
    ) -> str:
        """Generate a natural language summary of operational data."""
        
        if summary_type == "daily":
            return self._generate_daily_summary(data)
        elif summary_type == "weekly":
            return self._generate_weekly_summary(data)
        else:
            return self._generate_general_summary(data)
    
    def answer_question(
        self,
        question: str,
        data_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Answer a specific question about operations."""
        
        intent = self._classify_intent(question)
        entities = self._extract_entities(question)
        
        # Generate answer based on question type and available data
        answer = self._generate_answer(question, intent, entities, data_context or {})
        
        return answer
    
    def get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()
    
    def _classify_intent(self, message: str) -> str:
        """Classify the intent of a message."""
        message_lower = message.lower()
        
        for intent, pattern in self.intent_patterns.items():
            if re.search(pattern, message_lower):
                return intent
        
        return "general"
    
    def _extract_entities(self, message: str) -> Dict[str, Any]:
        """Extract entities (sources, time periods, metrics) from message."""
        entities = {}
        message_lower = message.lower()
        
        # Extract time references
        if "today" in message_lower:
            entities["time_period"] = "today"
        elif "yesterday" in message_lower:
            entities["time_period"] = "yesterday"
        elif "week" in message_lower:
            entities["time_period"] = "week"
        elif "month" in message_lower:
            entities["time_period"] = "month"
        
        # Extract sources
        source_match = re.search(r"(machine|shift|agent)[\s-]?(\w+)", message_lower)
        if source_match:
            entities["source"] = f"{source_match.group(1)}-{source_match.group(2)}"
        
        # Extract metric types
        metric_keywords = {
            "utilization": "UTILIZATION",
            "throughput": "THROUGHPUT",
            "idle": "IDLE_TIME",
            "quality": "QUALITY_SCORE",
            "downtime": "DOWNTIME",
        }
        for keyword, metric_type in metric_keywords.items():
            if keyword in message_lower:
                entities["metric_type"] = metric_type
                break
        
        return entities
    
    def _generate_response(
        self,
        intent: str,
        message: str,
        context: Dict[str, Any],
        entities: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate a response based on intent and context."""
        
        anomalies = context.get("recentAnomalies", [])
        incidents = context.get("recentIncidents", [])
        recommendations = context.get("pendingRecommendations", [])
        
        if intent == "status":
            return self._status_response(anomalies, incidents, recommendations)
        elif intent == "anomaly":
            return self._anomaly_response(anomalies, entities)
        elif intent == "loss":
            return self._loss_response(incidents)
        elif intent == "recommendation":
            return self._recommendation_response(recommendations)
        elif intent == "explain":
            return self._explain_response(message, anomalies, incidents)
        elif intent == "help":
            return self._help_response()
        else:
            return self._general_response()
    
    def _status_response(self, anomalies: list, incidents: list, recommendations: list) -> Dict:
        """Generate status overview response."""
        message = f"""📊 **Current Operational Status**

Based on my analysis of your operations:

• **Anomalies:** {len(anomalies)} detected recently
• **Active Incidents:** {len(incidents)} requiring attention  
• **Pending Optimizations:** {len(recommendations)} recommendations available

"""
        if len(anomalies) > 0:
            message += f"⚠️ Most recent anomaly: {anomalies[0].get('description', 'Unknown')} on {anomalies[0].get('source', 'Unknown source')}\n\n"
        
        if len(recommendations) > 0:
            message += f"💡 Top recommendation: {recommendations[0].get('title', 'Review pending actions')}\n"
        
        return {
            "message": message,
            "actions": ["View anomaly details", "Review recommendations", "Generate report"],
        }
    
    def _anomaly_response(self, anomalies: list, entities: Dict) -> Dict:
        """Generate anomaly-focused response."""
        if not anomalies:
            return {
                "message": "✅ No significant anomalies detected in your operations. Systems are running within normal parameters.",
                "actions": ["Set up custom alerts", "View historical trends"],
            }
        
        source_filter = entities.get("source")
        filtered = [a for a in anomalies if not source_filter or source_filter in a.get("source", "")] if source_filter else anomalies
        
        if not filtered:
            return {
                "message": f"No anomalies found for the specified source. However, {len(anomalies)} anomalies exist in other areas.",
                "actions": ["View all anomalies", "Change filter"],
            }
        
        latest = filtered[0]
        message = f"""🔍 **Anomaly Analysis**

**Latest Detection:**
• **Type:** {latest.get('anomalyType', 'Unknown').replace('_', ' ')}
• **Source:** {latest.get('source', 'Unknown')}
• **Severity:** {latest.get('severity', 'Unknown')}
• **Deviation:** {abs(latest.get('deviation', 0)):.1f}% from expected

**Description:** {latest.get('description', 'No description available')}

Total anomalies in view: {len(filtered)}
"""
        
        return {
            "message": message,
            "actions": ["Investigate root cause", "View all anomalies", "Mark as resolved"],
        }
    
    def _loss_response(self, incidents: list) -> Dict:
        """Generate loss analysis response."""
        if not incidents:
            return {
                "message": "💰 No significant losses recorded in the recent period. Operations are running efficiently!",
                "actions": ["View efficiency report", "Set loss alerts"],
            }
        
        total_loss = sum(i.get("estimatedLoss", 0) for i in incidents)
        active_count = len([i for i in incidents if i.get("status") in ["ACTIVE", "INVESTIGATING"]])
        
        message = f"""💰 **Loss Analysis**

In the recent period, I've identified:

• **Total Estimated Loss:** ₹{total_loss:,.0f}
• **Active Incidents:** {active_count}
• **Total Incidents:** {len(incidents)}

**Top Contributors:**
"""
        for i, incident in enumerate(incidents[:3], 1):
            message += f"{i}. {incident.get('title', 'Unknown')} - ₹{incident.get('estimatedLoss', 0):,.0f}\n"
        
        message += "\nI can help you prioritize which areas to focus on first."
        
        return {
            "message": message,
            "actions": ["View detailed breakdown", "Generate optimization plan", "Schedule review"],
        }
    
    def _recommendation_response(self, recommendations: list) -> Dict:
        """Generate recommendation response."""
        if not recommendations:
            return {
                "message": "✨ No pending recommendations at the moment. Your operations are optimized!",
                "actions": ["Request new analysis", "View completed actions"],
            }
        
        top_rec = recommendations[0]
        message = f"""💡 **Top Optimization Recommendation**

**{top_rec.get('title', 'Optimization Available')}**

{top_rec.get('description', 'No description')}

• **Estimated Impact:** ₹{top_rec.get('estimatedImpact', 0):,.0f}
• **Priority:** {top_rec.get('priority', 'Medium')}
• **Confidence:** {(top_rec.get('confidence', 0.8) * 100):.0f}%

**Reasoning:** {top_rec.get('reasoning', 'Based on operational analysis')}

Would you like me to execute this recommendation?
"""
        
        return {
            "message": message,
            "actions": ["Execute recommendation", "View all recommendations", "Get more details"],
        }
    
    def _explain_response(self, message: str, anomalies: list, incidents: list) -> Dict:
        """Generate explanation response."""
        # Try to identify what needs explanation
        if anomalies:
            latest = anomalies[0]
            return {
                "message": f"""📋 **Explanation for Recent Anomaly**

The {latest.get('anomalyType', 'unknown').replace('_', ' ').lower()} on {latest.get('source', 'unknown')} 
occurred because the measured value ({latest.get('value', 0):.1f}) deviated {abs(latest.get('deviation', 0)):.1f}% 
from the expected baseline ({latest.get('expectedValue', 0):.1f}).

**Possible Causes:**
• Operational variance during peak periods
• Resource constraint or equipment issue
• Process parameter drift

**Recommended Investigation:**
1. Review logs from the affected source
2. Check for correlated events
3. Monitor for pattern recurrence
""",
                "actions": ["Deep dive analysis", "View similar incidents", "Set up monitoring"],
            }
        
        return {
            "message": "I'd be happy to explain! Could you specify which anomaly, incident, or metric you'd like me to analyze?",
            "actions": ["View recent anomalies", "View incidents", "Ask another question"],
        }
    
    def _help_response(self) -> Dict:
        """Generate help response."""
        return {
            "message": """🧠 **I'm AOIA, your Autonomous Operational Intelligence Agent**

I can help you with:

📊 **Status & Overview**
"What's the current status?" | "Give me an overview"

🔍 **Anomaly Detection**
"What anomalies were detected?" | "Show issues on machine-1"

💰 **Loss Analysis**
"How much are we losing?" | "What's the cost of downtime?"

💡 **Recommendations**
"What do you suggest?" | "How can we optimize?"

📋 **Explanations**
"Why did throughput drop?" | "Explain the latest incident"

Just ask me anything about your operations!
""",
            "actions": ["Show status", "View anomalies", "Get recommendations"],
        }
    
    def _general_response(self) -> Dict:
        """Generate general response."""
        return {
            "message": """I'm here to help with your operational intelligence needs! 

You can ask me about:
• Current operational status
• Detected anomalies and issues
• Financial impact and losses
• Optimization recommendations
• Root cause analysis

What would you like to know?""",
            "actions": ["Show status", "View anomalies", "Get recommendations"],
        }
    
    def _explain_anomaly(self, entity: Dict, context: Optional[Dict]) -> Dict:
        """Generate detailed anomaly explanation."""
        anomaly_type = entity.get("anomalyType", "UNKNOWN").replace("_", " ")
        source = entity.get("source", "unknown")
        value = entity.get("value", 0)
        expected = entity.get("expectedValue", 0)
        deviation = entity.get("deviation", 0)
        
        explanation = f"""## Root Cause Analysis: {anomaly_type}

### Overview
A **{anomaly_type.lower()}** was detected on **{source}** with a deviation of **{abs(deviation):.1f}%** from expected values.

### Measurements
- **Observed Value:** {value:.2f}
- **Expected Value:** {expected:.2f}
- **Deviation:** {deviation:+.1f}%

### Analysis
The anomaly indicates a significant departure from normal operational patterns. This type of event typically occurs when:

1. **Operational Stress** - The resource is operating outside optimal parameters
2. **External Factors** - Environmental or upstream changes affecting performance
3. **Equipment Condition** - Potential maintenance needs or calibration drift

### Impact Assessment
Based on the severity and duration, this anomaly may result in:
- Reduced operational efficiency
- Potential quality implications
- Cascading effects on dependent processes

### Recommendations
1. Investigate the specific source for immediate issues
2. Review recent changes or events that may correlate
3. Consider preventive measures to avoid recurrence
"""
        
        return {
            "explanation": explanation,
            "key_findings": [
                f"Deviation of {abs(deviation):.1f}% from expected baseline",
                f"Source: {source}",
                f"Anomaly type: {anomaly_type}",
            ],
            "root_cause": "Operational variance requiring investigation",
            "confidence": 0.82,
        }
    
    def _explain_incident(self, entity: Dict, context: Optional[Dict]) -> Dict:
        """Generate detailed incident explanation."""
        title = entity.get("title", "Unknown Incident")
        description = entity.get("description", "No description")
        loss = entity.get("estimatedLoss", 0)
        status = entity.get("status", "UNKNOWN")
        
        explanation = f"""## Incident Analysis: {title}

### Summary
**Status:** {status}
**Estimated Impact:** ₹{loss:,.0f}

### Description
{description}

### Timeline Analysis
This incident represents a significant operational event that has been flagged for attention.

### Financial Impact
The estimated loss of ₹{loss:,.0f} includes:
- Direct productivity loss
- Resource inefficiency
- Potential downstream effects

### Resolution Pathway
1. **Immediate:** Acknowledge and begin investigation
2. **Short-term:** Implement recommended optimizations
3. **Long-term:** Review and update operational protocols to prevent recurrence
"""
        
        return {
            "explanation": explanation,
            "key_findings": [
                f"Estimated loss: ₹{loss:,.0f}",
                f"Current status: {status}",
                title,
            ],
            "root_cause": entity.get("rootCause", "Under investigation"),
            "confidence": 0.78,
        }
    
    def _generate_daily_summary(self, data: Dict) -> str:
        """Generate daily operational summary."""
        return f"""## Daily Operations Summary

**Date:** {datetime.now().strftime('%Y-%m-%d')}

### Key Metrics
- Operations analyzed: {data.get('metrics_count', 'N/A')}
- Anomalies detected: {data.get('anomalies_count', 0)}
- Active incidents: {data.get('incidents_count', 0)}

### Status
Overall operations are running within acceptable parameters with minor deviations noted.

### Recommendations
Review pending optimization suggestions to improve efficiency.
"""
    
    def _generate_weekly_summary(self, data: Dict) -> str:
        """Generate weekly operational summary."""
        return f"""## Weekly Operations Report

**Period:** Last 7 days

### Performance Overview
Your operations showed consistent performance with opportunities for optimization identified.

### Key Insights
- Total anomalies: {data.get('weekly_anomalies', 0)}
- Efficiency score: {data.get('efficiency_score', 85)}%
- Recommendations implemented: {data.get('actions_completed', 0)}

### Focus Areas
Continue monitoring highlighted areas for sustained improvement.
"""
    
    def _generate_general_summary(self, data: Dict) -> str:
        """Generate general summary."""
        return "Operations summary: System is functioning within normal parameters. Review dashboard for detailed metrics."
    
    def _generate_answer(
        self,
        question: str,
        intent: str,
        entities: Dict,
        data_context: Dict,
    ) -> Dict:
        """Generate an answer to a specific question."""
        return {
            "answer": f"Based on my analysis, I can provide insights about your {intent} query. The requested information has been analyzed from available operational data.",
            "confidence": 0.85,
            "data_sources": ["Real-time metrics", "Historical patterns", "Anomaly database"],
        }
