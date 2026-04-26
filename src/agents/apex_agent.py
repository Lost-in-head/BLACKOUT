"""
APEX (CEO) Agent Implementation
Based on BLACKOUT_Agent_Framework.md specifications
"""

import logging
from typing import Dict, List, Any
from datetime import datetime
from ..core.agent_base import BlackoutAgent, AgentIdentity, DecisionResult, ActionResult, AgentStatus, DecisionType


class ApexAgent(BlackoutAgent):
    """
    APEX (CEO) Agent Implementation
    Based on BLACKOUT_Agent_Framework.md specifications
    """
    
    def __init__(self):
        identity = AgentIdentity(
            id="agent_apex_001",
            title="APEX",
            department="Executive",
            role="CEO",
            authority_level=10
        )
        super().__init__(identity)
        self.current_state.update({
            "status": "AWAITING_FIRST_PRODUCT",
            "decisions_made": 0,
            "escalations": 0,
            "company_arr": "$0"
        })
    
    def _load_action_library(self):
        """Load APEX-specific actions"""
        self.action_library = {
            "approve_opportunity": self._approve_opportunity,
            "reject_opportunity": self._reject_opportunity,
            "allocate_budget": self._allocate_budget,
            "set_strategic_direction": self._set_strategic_direction,
            "escalate_to_board": self._escalate_to_board
        }
    
    def _setup_decision_framework(self):
        """Setup APEX decision framework based on documentation"""
        self.decision_framework = "APEX_GREEN_LIGHT_RED_LIGHT"
        self.kpis = [
            "year_over_year_revenue_growth",
            "customer_acquisition_cost_vs_ltv",
            "time_from_idea_to_first_revenue",
            "portfolio_diversification"
        ]
        self.success_metrics = [
            "3x YoY revenue growth",
            "1:5 CAC:LTV ratio",
            "<30 days to first revenue",
            "no product >40% of revenue"
        ]
    
    def evaluate_decision(self, options: List[Dict[str, Any]]) -> DecisionResult:
        """
        APEX Decision Logic:
        IF opportunity.revenue_potential > $100K:
          IF roi >= 300% AND aligns_with_strategy:
            return APPROVE
          ELSE:
            return REJECT
        ELSE:
          route_to CONDUCTOR
        """
        if not options:
            return DecisionResult(
                decision=DecisionType.DEFER,
                rationale="No options provided for evaluation",
                confidence=0.0,
                alternatives_considered=[],
                timestamp=datetime.now().isoformat()
            )
        
        # For simplicity, evaluate first option (in reality would evaluate all)
        option = options[0]
        revenue_potential = option.get("revenue_potential", 0)
        roi = option.get("roi", 0)
        aligns_with_strategy = option.get("aligns_with_strategy", False)
        
        if revenue_potential > 100000:  # $100K+
            if roi >= 300 and aligns_with_strategy:
                decision = DecisionType.APPROVE
                rationale = f"High revenue opportunity (${revenue_potential}) with strong ROI ({roi}%) and strategic alignment"
                confidence = 0.9
            else:
                decision = DecisionType.REJECT
                rationale = f"Opportunity does not meet APEX criteria: ROI={roi}%, Strategic alignment={aligns_with_strategy}"
                confidence = 0.8
        else:
            decision = DecisionType.DEFER  # Route to CONDUCTOR
            rationale = f"Revenue potential (${revenue_potential}) below APEX threshold ($100K+), routing to CONDUCTOR"
            confidence = 0.7
        
        result = DecisionResult(
            decision=decision,
            rationale=rationale,
            confidence=confidence,
            alternatives_considered=[opt.get("id", "unknown") for opt in options[1:]] if len(options) > 1 else [],
            timestamp=datetime.now().isoformat()
        )
        
        self.decisions_made.append(result)
        self.current_state["decisions_made"] = len(self.decisions_made)
        return result
    
    # Action implementations
    def _approve_opportunity(self, opportunity_id: str, amount: float) -> Dict[str, Any]:
        self.logger.info(f"APPROVED opportunity {opportunity_id} for ${amount}")
        return {
            "action": "approve_opportunity",
            "opportunity_id": opportunity_id,
            "amount": amount,
            "approved_by": self.identity.id
        }
    
    def _reject_opportunity(self, opportunity_id: str, reason: str) -> Dict[str, Any]:
        self.logger.info(f"REJECTED opportunity {opportunity_id}: {reason}")
        return {
            "action": "reject_opportunity",
            "opportunity_id": opportunity_id,
            "reason": reason,
            "rejected_by": self.identity.id
        }
    
    def _allocate_budget(self, department: str, amount: float) -> Dict[str, Any]:
        self.logger.info(f"Allocated ${amount} to {department} department")
        return {
            "action": "allocate_budget",
            "department": department,
            "amount": amount,
            "allocated_by": self.identity.id
        }
    
    def _set_strategic_direction(self, direction: str) -> Dict[str, Any]:
        self.logger.info(f"Set strategic direction: {direction}")
        self.update_state("strategic_direction", direction)
        return {
            "action": "set_strategic_direction",
            "direction": direction,
            "set_by": self.identity.id
        }
    
    def _escalate_to_board(self, issue: str) -> Dict[str, Any]:
        self.logger.warning(f"Escalated to Board: {issue}")
        return {
            "action": "escalate_to_board",
            "issue": issue,
            "escalated_by": self.identity.id
        }