"""
AOIA ML Engine - Autonomy Modes
Defines the three operational modes for AOIA.
"""

from enum import Enum
from typing import Dict, Any


class AutonomyMode(str, Enum):
    """
    AOIA Autonomy Modes
    
    ASSIST: Detection + Explanation + Recommendation only (no execution)
    COPILOT: Asks for approval before executing actions
    FULL_AUTO: Complete autonomous operation - detect, reason, plan, execute
    """
    ASSIST = "ASSIST"
    COPILOT = "COPILOT"
    FULL_AUTO = "FULL_AUTO"
    
    @classmethod
    def from_string(cls, mode_str: str) -> "AutonomyMode":
        """Parse mode from string, defaulting to FULL_AUTO."""
        mode_str = mode_str.upper().strip()
        try:
            return cls(mode_str)
        except ValueError:
            return cls.FULL_AUTO


class ModeConfig:
    """Configuration for each autonomy mode."""
    
    CONFIGS: Dict[AutonomyMode, Dict[str, Any]] = {
        AutonomyMode.ASSIST: {
            "can_detect": True,
            "can_reason": True,
            "can_estimate_loss": True,
            "can_plan": True,
            "can_execute": False,
            "requires_approval": False,
            "description": "Detection and recommendations only - no automatic execution"
        },
        AutonomyMode.COPILOT: {
            "can_detect": True,
            "can_reason": True,
            "can_estimate_loss": True,
            "can_plan": True,
            "can_execute": True,
            "requires_approval": True,
            "description": "Full analysis with execution after human approval"
        },
        AutonomyMode.FULL_AUTO: {
            "can_detect": True,
            "can_reason": True,
            "can_estimate_loss": True,
            "can_plan": True,
            "can_execute": True,
            "requires_approval": False,
            "description": "Fully autonomous operation - detect, analyze, execute"
        },
    }
    
    @classmethod
    def get_config(cls, mode: AutonomyMode) -> Dict[str, Any]:
        """Get configuration for a mode."""
        return cls.CONFIGS.get(mode, cls.CONFIGS[AutonomyMode.FULL_AUTO])
    
    @classmethod
    def can_execute(cls, mode: AutonomyMode) -> bool:
        """Check if mode allows execution."""
        return cls.get_config(mode).get("can_execute", False)
    
    @classmethod
    def requires_approval(cls, mode: AutonomyMode) -> bool:
        """Check if mode requires approval for execution."""
        return cls.get_config(mode).get("requires_approval", False)
