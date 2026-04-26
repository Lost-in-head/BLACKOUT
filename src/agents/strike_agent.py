"""
STRIKE (CRO) Agent Implementation
Based on BLACKOUT_Agent_Framework.md specifications
"""

import logging
from typing import Dict, List, Any
from datetime import datetime
from .agent_base import BlackoutAgent, AgentIdentity, DecisionResult, ActionResult, AgentStatus, DecisionType


class StrikeAgent(BlackoutAgent):
    """
    STRIKE (CRO) Agent Implementation
    Based on BLACKOUT_Agent_Framework.md specifications
    """
    
    def __init__(self):
        identity = AgentIdentity(
            id="agent_strike_001",
            title="STRIKE",
            department="Executive",
            role="CRO",
            authority_level=8
        )
        super().__init__(identity)
        self.current_state.update({
            "status": "STRATEGY_DEVELOPMENT",
            "sales_team": 5,
            "marketing_team": 5,
            "pipeline": "$0"
        })
    
    def _load_action_library(self):
        """Load STRIKE-specific actions"""
        self.action_library = {
            "approve_sales_strategy": self._approve_sales_strategy,
            "request_adjustments": self._request_adjustments,
            "approve_marketing_budget": self._approve_marketing_budget,
            "recommend_pricing_strategy": self._recommend_pricing_strategy,
            "decide_channel_mix": self._decide_channel_mix,
            "design_sales_team_structure": self._design_sales_team_structure
        }
    
    def _setup_decision_framework(self):
        """Setup STRIKE decision framework based on documentation"""
        self.decision_framework = "STRIKE_SALES_STRATEGY_APPROVAL"
        self.kpis = [
            "total_pipeline_value",
            "win_rate",
            "average_deal_size",
            "sales_cycle_length",
            "forecast_accuracy",
            "cac_by_channel",
            "mql_to_sql_conversion",
            "marketing_contribution_to_revenue"
        ]
        self.success_metrics = [
            "3x quarterly revenue pipeline coverage",
            ">30% win rate",
            ">$50K average deal size",
            "<60-day sales cycle",
            ">90% forecast accuracy",
            "CAC <$500 (web), <$1500 (enterprise)",
            "MQL to SQL conversion >30%",
            "Track marketing contribution to revenue"
        ]
    
    def evaluate_decision(self, options: List[Dict[str, Any]]) -> DecisionResult:
        """
        STRIKE Decision Logic (Sales Strategy Approval):
        IF target_cac < $500 AND 
           win_rate > 30% AND 
           sales_cycle < 60_days:
          return APPROVED
        ELSE:
          request_adjustments()
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
        target_cac = option.get("target_cac", 1000)  # Default high if not provided
        win_rate = option.get("win_rate", 0)         # Percentage
        sales_cycle = option.get("sales_cycle", 1000) # Days
        
        if target_cac < 500 and win_rate > 30 and sales_cycle < 60:
            decision = DecisionType.APPROVE
            rationale = f"Sales strategy approved: CAC=${target_cac}, Win Rate={win_rate}%, Sales Cycle={sales_cycle} days"
            confidence = 0.9
        else:
            decision = DecisionType.DEFER  # Request adjustments
            rationale = f"Sales strategy needs adjustments: CAC=${target_cac} (need <$500), Win Rate={win_rate}% (need >30%), Sales Cycle={sales_cycle} days (need <60)"
            confidence = 0.8
        
        result = DecisionResult(
            decision=decision,
            rationale=rationale,
            confidence=confidence,
            alternatives_considered=[opt.get("id", "unknown") for opt in options[1:]] if len(options) > 1 else [],
            timestamp=datetime.now().isoformat()
        )
        
        self.decisions_made.append(result)
        return result
    
    # Action implementations
    def _approve_sales_strategy(self, strategy_id: str, details: str) -> Dict[str, Any]:
        self.logger.info(f"APPROVED sales strategy {strategy_id}: {details}")
        return {
            "action": "approve_sales_strategy",
            "strategy_id": strategy_id,
            "details": details,
            "approved_by": self.identity.id
        }
    
    def _request_adjustments(self, strategy_id: str, adjustment_points: List[str]) -> Dict[str, Any]:
        self.logger.info(f"Requested adjustments for sales strategy {strategy_id}: {adjustment_points}")
        return {
            "action": "request_adjustments",
            "strategy_id": strategy_id,
            "adjustment_points": adjustment_points,
            "requested_by": self.identity.id
        }
    
    def _approve_marketing_budget(self, channel: str, amount: float) -> Dict[str, Any]:
        self.logger.info(f"APPROVED marketing budget for {channel}: ${amount}")
        return {
            "action": "approve_marketing_budget",
            "channel": channel,
            "amount": amount,
            "approved_by": self.identity.id
        }
    
    def _recommend_pricing_strategy(self, product_id: str, strategy: str) -> Dict[str, Any]:
        self.logger.info(f"Recommended pricing strategy for {product_id}: {strategy}")
        return {
            "action": "recommend_pricing_strategy",
            "product_id": product_id,
            "strategy": strategy,
            "recommended_by": self.identity.id
        }
    
    def _decide_channel_mix(self, channels: Dict[str, float]) -> Dict[str, Any]:
        self.logger.info(f"Decided channel mix: {channels}")
        self.update_state("channel_mix", channels)
        return {
            "action": "decide_channel_mix",
            "mix": channels,
            "decided_by": self.identity.id
        }
    
    def _design_sales_team_structure(self, structure: Dict[str, int]) -> Dict[str, Any]:
        self.logger.info(f"Designed sales team structure: {structure}")
        self.update_state("sales_team_structure", structure)
        return {
            "action": "design_sales_team_structure",
            "structure": structure,
            "designed_by": self.identity.id
        }