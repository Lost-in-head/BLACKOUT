"""
VISION (CPO) Agent Implementation
Based on BLACKOUT_Agent_Framework.md specifications
"""

import logging
from typing import Dict, List, Any
from datetime import datetime
from .agent_base import BlackoutAgent, AgentIdentity, DecisionResult, ActionResult, AgentStatus, DecisionType


class VisionAgent(BlackoutAgent):
    """
    VISION (CPO) Agent Implementation
    Based on BLACKOUT_Agent_Framework.md specifications
    """
    
    def __init__(self):
        identity = AgentIdentity(
            id="agent_vision_001",
            title="VISION",
            department="Executive",
            role="CPO",
            authority_level=8
        )
        super().__init__(identity)
        self.current_state.update({
            "status": "PRODUCT_STRATEGY_FORMATION",
            "product_team": 4,
            "support_team": 3
        })
    
    def _load_action_library(self):
        """Load VISION-specific actions"""
        self.action_library = {
            "prioritize_features": self._prioritize_features,
            "manage_roadmap": self._manage_roadmap,
            "conduct_user_research": self._conduct_user_research,
            "define_success_metrics": self._define_success_metrics,
            "approve_design_direction": self._approve_design_direction,
            "approve_user_testing": self._approve_user_testing
        }
    
    def _setup_decision_framework(self):
        """Setup VISION decision framework based on documentation"""
        self.decision_framework = "VISION_FEATURE_PRIORIZATION"
        self.kpis = [
            "feature_adoption_rate",
            "feature_satisfaction_nps",
            "revenue_per_feature",
            "user_retention_post_launch"
        ]
        self.success_metrics = [
            ">60% feature adoption rate",
            "NPS >8/10",
            "Track revenue contribution per feature",
            "+10% user retention post-feature launch"
        ]
    
    def evaluate_decision(self, options: List[Dict[str, Any]]) -> DecisionResult:
        """
        VISION Decision Logic (Feature Prioritization):
        FOR each feature:
          score = (revenue_impact × 0.5) + 
                 (user_impact × 0.3) + 
                 (effort_factor × 0.2)
        RETURN sorted_by_score
        """
        if not options:
            return DecisionResult(
                decision=DecisionType.DEFER,
                rationale="No options provided for evaluation",
                confidence=0.0,
                alternatives_considered=[],
                timestamp=datetime.now().isoformat()
            )
        
        # Score each option and return the highest scoring one
        scored_options = []
        for option in options:
            revenue_impact = option.get("revenue_impact", 0)  # 0-10 scale
            user_impact = option.get("user_impact", 0)       # 0-10 scale
            effort_factor = option.get("effort_factor", 10)  # 0-10 scale (lower is better)
            
            # Normalize effort factor (invert so lower effort = higher score)
            normalized_effort = max(0, 10 - effort_factor)
            
            score = (revenue_impact * 0.5) + (user_impact * 0.3) + (normalized_effort * 0.2)
            scored_options.append((option, score))
        
        # Sort by score descending
        scored_options.sort(key=lambda x: x[1], reverse=True)
        best_option, best_score = scored_options[0]
        
        decision = DecisionType.APPROVE
        rationale = f"Feature prioritized with score {best_score:.2f}: {best_option.get('description', 'Unknown feature')}"
        confidence = min(0.95, 0.7 + (best_score / 20))  # Scale confidence with score
        
        result = DecisionResult(
            decision=decision,
            rationale=rationale,
            confidence=confidence,
            alternatives_considered=[opt.get("id", "unknown") for opt, _ in scored_options[1:]],
            timestamp=datetime.now().isoformat()
        )
        
        self.decisions_made.append(result)
        return result
    
    # Action implementations
    def _prioritize_features(self, features: List[Dict[str, Any]]) -> Dict[str, Any]:
        self.logger.info(f"Prioritizing {len(features)} features")
        # Sort by VISION's prioritization framework
        scored_features = []
        for feature in features:
            revenue_impact = feature.get("revenue_impact", 0)
            user_impact = feature.get("user_impact", 0)
            effort_factor = feature.get("effort_factor", 10)
            normalized_effort = max(0, 10 - effort_factor)
            score = (revenue_impact * 0.5) + (user_impact * 0.3) + (normalized_effort * 0.2)
            scored_features.append((feature, score))
        
        scored_features.sort(key=lambda x: x[1], reverse=True)
        prioritized = [feature for feature, score in scored_features]
        
        return {
            "action": "prioritize_features",
            "prioritized_features": prioritized,
            "prioritized_by": self.identity.id
        }
    
    def _manage_roadmap(self, roadmap_updates: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info(f"Managing roadmap updates: {list(roadmap_updates.keys())}")
        self.update_state("roadmap", roadmap_updates)
        return {
            "action": "manage_roadmap",
            "updates": roadmap_updates,
            "managed_by": self.identity.id
        }
    
    def _conduct_user_research(self, research_type: str, participant_count: int) -> Dict[str, Any]:
        self.logger.info(f"Conducting {research_type} user research with {participant_count} participants")
        return {
            "action": "conduct_user_research",
            "research_type": research_type,
            "participant_count": participant_count,
            "conducted_by": self.identity.id
        }
    
    def _define_success_metrics(self, feature_id: str, metrics: List[str]) -> Dict[str, Any]:
        self.logger.info(f"Defined success metrics for feature {feature_id}: {metrics}")
        return {
            "action": "define_success_metrics",
            "feature_id": feature_id,
            "metrics": metrics,
            "defined_by": self.identity.id
        }
    
    def _approve_design_direction(self, design_id: str, direction: str) -> Dict[str, Any]:
        self.logger.info(f"Approved design direction for {design_id}: {direction}")
        return {
            "action": "approve_design_direction",
            "design_id": design_id,
            "direction": direction,
            "approved_by": self.identity.id
        }
    
    def _approve_user_testing(self, test_plan: str) -> Dict[str, Any]:
        self.logger.info(f"Approved user testing: {test_plan}")
        return {
            "action": "approve_user_testing",
            "test_plan": test_plan,
            "approved_by": self.identity.id
        }