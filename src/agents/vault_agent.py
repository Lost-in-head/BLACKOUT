"""
VAULT (CFO) Agent Implementation
Based on BLACKOUT_Agent_Framework.md specifications
"""

import logging
from typing import Dict, List, Any
from datetime import datetime
from .agent_base import BlackoutAgent, AgentIdentity, DecisionResult, ActionResult, AgentStatus, DecisionType


class VaultAgent(BlackoutAgent):
    """
    VAULT (CFO) Agent Implementation
    Based on BLACKOUT_Agent_Framework.md specifications
    """
    
    def __init__(self):
        identity = AgentIdentity(
            id="agent_vault_001",
            title="VAULT",
            department="Executive",
            role="CFO",
            authority_level=8
        )
        super().__init__(identity)
        self.current_state.update({
            "status": "MONITORING",
            "cash_position": "$0",
            "runway_months": 0
        })
    
    def _load_action_library(self):
        """Load VAULT-specific actions"""
        self.action_library = {
            "auto_approve_expense": self._auto_approve_expense,
            "approve_expense": self._approve_expense,
            "reject_expense": self._reject_expense,
            "escalate_to_apex": self._escalate_to_apex,
            "track_financial_metrics": self._track_financial_metrics,
            "manage_cash_flow": self._manage_cash_flow
        }
    
    def _setup_decision_framework(self):
        """Setup VAULT decision framework based on documentation"""
        self.decision_framework = "VAULT_SPENDING_DECISION"
        self.kpis = [
            "monthly_burn_rate",
            "months_of_runway",
            "customer_lifetime_value",
            "cac_payback_period",
            "gross_margin"
        ]
        self.success_metrics = [
            "<$100K/month burn rate at scale",
            "12+ months runway",
            ">$50K customer lifetime value",
            "<6 months CAC payback period",
            ">70% gross margin"
        ]
    
    def evaluate_decision(self, options: List[Dict[str, Any]]) -> DecisionResult:
        """
        VAULT Decision Logic (Spending Decision):
        IF amount < $10K:
          return AUTO_APPROVE
        ELSE IF amount < $50K:
          IF roi_positive AND cash_safe:
            return APPROVE
          ELSE:
            return REJECT
        ELSE:
          escalate_to(APEX)
        """
        if not options:
            return DecisionResult(
                decision=DecisionType.DEFER,
                rationale="No options provided for evaluation",
                confidence=0.0,
                alternatives_considered=[],
                timestamp=datetime.now().isoformat()
            )
        
        option = options[0]
        amount = option.get("amount", 0)
        roi_positive = option.get("roi_positive", False)
        cash_safe = option.get("cash_safe", False)
        
        if amount < 10000:  # < $10K
            decision = DecisionType.APPROVE  # AUTO_APPROVE
            rationale = f"Expense amount (${amount}) below auto-approve threshold ($10K)"
            confidence = 0.95
        elif amount < 50000:  # < $50K
            if roi_positive and cash_safe:
                decision = DecisionType.APPROVE
                rationale = f"Expense amount (${amount}) approved: ROI positive and cash position safe"
                confidence = 0.9
            else:
                decision = DecisionType.REJECT
                rationale = f"Expense amount (${amount}) rejected: ROI positive={roi_positive}, cash safe={cash_safe}"
                confidence = 0.85
        else:
            decision = DecisionType.ESCALATE  # escalate_to(APEX)
            rationale = f"Expense amount (${amount}) exceeds VAULT authority (>= $50K), escalating to APEX"
            confidence = 0.9
        
        result = DecisionResult(
            decision=decision,
            rationale=rationale,
            confidence=confidence,
            alternatives_considered=[opt.get("id", "unknown") for opt in options[1:]] if len(options) > 1 else [],
            timestamp=datetime.now().isoformat()
        )
        
        self.decisions_made.append(result)
        # Update financial state if available
        if "cash_position" in option:
            self.current_state["cash_position"] = option["cash_position"]
        if "runway_months" in option:
            self.current_state["runway_months"] = option["runway_months"]
        return result
    
    # Action implementations
    def _auto_approve_expense(self, expense_id: str, amount: float) -> Dict[str, Any]:
        self.logger.info(f"AUTO-APPROVED expense {expense_id} for ${amount}")
        return {
            "action": "auto_approve_expense",
            "expense_id": expense_id,
            "amount": amount,
            "approved_by": self.identity.id,
            "approval_type": "AUTO"
        }
    
    def _approve_expense(self, expense_id: str, amount: float, roi: float) -> Dict[str, Any]:
        self.logger.info(f"APPROVED expense {expense_id} for ${amount} (ROI: {roi}%)")
        return {
            "action": "approve_expense",
            "expense_id": expense_id,
            "amount": amount,
            "roi": roi,
            "approved_by": self.identity.id,
            "approval_type": "MANUAL"
        }
    
    def _reject_expense(self, expense_id: str, amount: float, reason: str) -> Dict[str, Any]:
        self.logger.info(f"REJECTED expense {expense_id} for ${amount}: {reason}")
        return {
            "action": "reject_expense",
            "expense_id": expense_id,
            "amount": amount,
            "reason": reason,
            "rejected_by": self.identity.id
        }
    
    def _escalate_to_apex(self, expense_id: str, amount: float) -> Dict[str, Any]:
        self.logger.warning(f"ESCALATED expense {expense_id} (${amount}) to APEX")
        return {
            "action": "escalate_to_apex",
            "expense_id": expense_id,
            "amount": amount,
            "escalated_by": self.identity.id
        }
    
    def _track_financial_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info(f"Tracking financial metrics: {list(metrics.keys())}")
        self.current_state.update(metrics)
        return {
            "action": "track_financial_metrics",
            "metrics": metrics,
            "tracked_by": self.identity.id
        }
    
    def _manage_cash_flow(self, inflow: float, outflow: float) -> Dict[str, Any]:
        net_flow = inflow - outflow
        self.logger.info(f"Managing cash flow: Inflow ${inflow}, Outflow ${outflow}, Net ${net_flow}")
        return {
            "action": "manage_cash_flow",
            "inflow": inflow,
            "outflow": outflow,
            "net_flow": net_flow,
            "managed_by": self.identity.id
        }