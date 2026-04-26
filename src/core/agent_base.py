"""
Base Agent Class for BLACKOUT Framework
Defines the common interface and functionality for all agents in the BLACKOUT system.
"""

import abc
import json
import logging
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


class AgentStatus(Enum):
    """Agent operational status"""
    INACTIVE = "inactive"
    ACTIVE = "active"
    BUSY = "busy"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class DecisionType(Enum):
    """Types of decisions an agent can make"""
    APPROVE = "approve"
    REJECT = "reject"
    ESCALATE = "escalate"
    DEFER = "defer"
    MODIFY = "modify"


@dataclass
class AgentIdentity:
    """Unique identification for an agent"""
    id: str
    title: str
    department: str
    role: str
    authority_level: int  # 1-10 scale


@dataclass
class DecisionResult:
    """Result of a decision-making process"""
    decision: DecisionType
    rationale: str
    confidence: float  # 0.0 to 1.0
    alternatives_considered: List[str]
    timestamp: str


@dataclass
class ActionResult:
    """Result of executing an action"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: str = None


class BlackoutAgent(abc.ABC):
    """
    Base class for all BLACKOUT agents.
    Implements the core framework described in BLACKOUT_Agent_Framework.md
    """
    
    def __init__(self, identity: AgentIdentity):
        self.identity = identity
        self.status = AgentStatus.INACTIVE
        self.decision_framework = None
        self.kpis: List[str] = []
        self.success_metrics: List[str] = []
        
        # Relationships
        self.reports_to: Optional['BlackoutAgent'] = None
        self.directly_manages: List['BlackoutAgent'] = []
        self.collaborates_with: List['BlackoutAgent'] = []
        self.depends_on: List['BlackoutAgent'] = []
        
        # Capabilities
        self.can_approve: List[str] = []
        self.can_reject: List[str] = []
        self.can_escalate_to: List['BlackoutAgent'] = []
        self.action_library: Dict[str, callable] = {}
        
        # State & Memory
        self.current_state: Dict[str, Any] = {}
        self.decisions_made: List[DecisionResult] = []
        self.actions_executed: List[ActionResult] = []
        
        # Setup logging
        self.logger = logging.getLogger(f"blackout.agent.{self.identity.id}")
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize agent-specific components"""
        self.status = AgentStatus.ACTIVE
        self.logger.info(f"Agent {self.identity.id} ({self.identity.title}) initialized")
        self._load_action_library()
        self._setup_decision_framework()
    
    @abc.abstractmethod
    def _load_action_library(self):
        """Load agent-specific actions into action_library"""
        pass
    
    @abc.abstractmethod
    def _setup_decision_framework(self):
        """Setup agent-specific decision-making framework"""
        pass
    
    @abc.abstractmethod
    def evaluate_decision(self, options: List[Dict[str, Any]]) -> DecisionResult:
        """
        Evaluate options and make a decision based on agent's framework
        """
        pass
    
    def take_action(self, action_name: str, **kwargs) -> ActionResult:
        """
        Execute an action from the agent's action library
        """
        if action_name not in self.action_library:
            return ActionResult(
                success=False,
                message=f"Action '{action_name}' not available for agent {self.identity.id}"
            )
        
        try:
            self.status = AgentStatus.BUSY
            result = self.action_library[action_name](**kwargs)
            self.status = AgentStatus.ACTIVE
            
            action_result = ActionResult(
                success=True,
                message=f"Action '{action_name}' executed successfully",
                data=result,
                timestamp=datetime.now().isoformat()
            )
            
            self.actions_executed.append(action_result)
            self.logger.info(f"Executed action: {action_name}")
            return action_result
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            self.logger.error(f"Error executing action {action_name}: {str(e)}")
            return ActionResult(
                success=False,
