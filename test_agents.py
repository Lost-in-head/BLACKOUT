#!/usr/bin/env python3
"""
Test script for BLACKOUT Agent Framework
Demonstrates the creation and basic usage of BLACKOUT agents.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.apex_agent import ApexAgent
from src.agents.conductor_agent import ConductorAgent
from src.agents.vault_agent import VaultAgent
from src.agents.oracle_agent import OracleAgent
from src.agents.forge_agent import ForgeAgent
from src.agents.vision_agent import VisionAgent
from src.agents.strike_agent import StrikeAgent
from src.agents.shield_agent import ShieldAgent
from src.agents.architect_agent import ArchitectAgent

def test_agent_creation():
    """Test that all agents can be created successfully"""
    print("Testing BLACKOUT Agent Framework...")
    print("=" * 50)
    
    agents = []
    
    # Create each agent type
    try:
        apex = ApexAgent()
        agents.append(apex)
        print(f"✓ Created {apex.identity.title} ({apex.identity.id})")
    except Exception as e:
        print(f"✗ Failed to create APEX agent: {e}")
    
    try:
        conductor = ConductorAgent()
        agents.append(conductor)
        print(f"✓ Created {conductor.identity.title} ({conductor.identity.id})")
    except Exception as e:
        print(f"✗ Failed to create CONDUCTOR agent: {e}")
    
    try:
        vault = VaultAgent()
        agents.append(vault)
        print(f"✓ Created {vault.identity.title} ({vault.identity.id})")
    except Exception as e:
        print(f"✗ Failed to create VAULT agent: {e}")
    
    try:
        oracle = OracleAgent()
        agents.append(oracle)
        print(f"✓ Created {oracle.identity.title} ({oracle.identity.id})")
    except Exception as e:
        print(f"✗ Failed to create ORACLE agent: {e}")
    
    try:
        forge = ForgeAgent()
        agents.append(forge)
        print(f"✓ Created {forge.identity.title} ({forge.identity.id})")
    except Exception as e:
        print(f"✗ Failed to create FORGE agent: {e}")
    
    try:
        vision = VisionAgent()
        agents.append(vision)
        print(f"✓ Created {vision.identity.title} ({vision.identity.id})")
    except Exception as e:
        print(f"✗ Failed to create VISION agent: {e}")
    
    try:
        strike = StrikeAgent()
        agents.append(strike)
        print(f"✓ Created {strike.identity.title} ({strike.identity.id})")
    except Exception as e:
        print(f"✗ Failed to create STRIKE agent: {e}")
    
    try:
        shield = ShieldAgent()
        agents.append(shield)
        print(f"✓ Created {shield.identity.title} ({shield.identity.id})")
    except Exception as e:
        print(f"✗ Failed to create SHIELD agent: {e}")
    
    try:
        architect = ArchitectAgent()
        agents.append(architect)
        print(f"✓ Created {architect.identity.title} ({architect.identity.id})")
    except Exception as e:
        print(f"✗ Failed to create ARCHITECT agent: {e}")
    
    print("=" * 50)
    print(f"Successfully created {len(agents)} agents")
    
    # Test agent status summary
    print("\nAgent Status Summaries:")
    print("-" * 30)
    for agent in agents:
        print(agent.get_status_summary())
        print()
    
    # Test decision making for APEX (example)
    print("Testing APEX Decision Making:")
    print("-" * 30)
    opportunity = {
        "id": "opp_001",
        "revenue_potential": 150000,
        "roi": 350,
        "aligns_with_strategy": True
    }
    
    decision = apex.evaluate_decision([opportunity])
    print(f"Opportunity: ${opportunity['revenue_potential']:,} revenue potential, {opportunity['roi']}% ROI, strategic alignment: {opportunity['aligns_with_strategy']}")
    print(f"Decision: {decision.decision.value}")
    print(f"Rationale: {decision.rationale}")
    print(f"Confidence: {decision.confidence:.2f}")
    
    # Test communication between agents
    print("\nTesting Agent Communication:")
    print("-" * 30)
    apex.communicate("Hello from APEX!", conductor)
    conductor.communicate("Received and processing", apex)
    print("✓ Communication test completed")
    
    print("\n" + "=" * 50)
    print("BLACKOUT Agent Framework Test Complete!")
    return len(agents) == 9  # We expect 9 agents

if __name__ == "__main__":
    success = test_agent_creation()
    sys.exit(0 if success else 1)