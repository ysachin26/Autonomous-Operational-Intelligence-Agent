"""
AOIA ML Engine - Base Agent
Abstract base class for all AOIA sub-agents.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
import logging


class BaseAgent(ABC):
    """
    Abstract base class for all AOIA agents.
    
    Provides common functionality:
    - Logging and metrics tracking
    - Inter-agent communication interface
    - Standard lifecycle methods
    """
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.agent_id = f"{agent_name}-{uuid.uuid4().hex[:8]}"
        self.logger = logging.getLogger(f"aoia.{agent_name}")
        self.metrics: Dict[str, Any] = {
            "total_runs": 0,
            "successful_runs": 0,
            "failed_runs": 0,
            "total_processing_time_ms": 0,
            "last_run": None,
        }
        self._status = "idle"
        self._last_output: Optional[Dict[str, Any]] = None
        self._message_queue: List[Dict[str, Any]] = []
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main processing method - must be implemented by each agent.
        
        Args:
            input_data: Input data specific to this agent
            context: Optional context from other agents or orchestrator
            
        Returns:
            Processing results
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "status": self._status,
            "metrics": self.metrics,
            "last_run": self.metrics.get("last_run"),
        }
    
    def send_message(self, target_agent: str, message: Dict[str, Any]) -> None:
        """Send a message to another agent via the orchestrator."""
        self._message_queue.append({
            "from": self.agent_name,
            "to": target_agent,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        })
    
    def receive_messages(self) -> List[Dict[str, Any]]:
        """Get and clear pending messages."""
        messages = self._message_queue.copy()
        self._message_queue.clear()
        return messages
    
    def _start_processing(self) -> datetime:
        """Mark processing start and return start time."""
        self._status = "processing"
        self.metrics["total_runs"] += 1
        return datetime.now()
    
    def _complete_processing(self, start_time: datetime, success: bool = True) -> None:
        """Mark processing complete and update metrics."""
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds() * 1000
        
        self._status = "idle"
        self.metrics["total_processing_time_ms"] += processing_time
        self.metrics["last_run"] = end_time.isoformat()
        
        if success:
            self.metrics["successful_runs"] += 1
        else:
            self.metrics["failed_runs"] += 1
    
    def _log_error(self, error: Exception, context: str = "") -> None:
        """Log an error with context."""
        self.logger.error(f"[{self.agent_name}] {context}: {str(error)}")
    
    def _log_info(self, message: str) -> None:
        """Log an info message."""
        self.logger.info(f"[{self.agent_name}] {message}")
