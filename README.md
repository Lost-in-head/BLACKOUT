# BLACKOUT Framework

An AI-agent organizational framework designed to simulate enterprise operations with specialized agents across executive and department levels.

## Overview

BLACKOUT Framework implements a hierarchical agent system modeled after a modern enterprise organization, featuring:
- 8 Executive Agents (C-suite level)
- 32 Specialist Agents across 8 departments
- Decision-making frameworks based on documented specifications
- Inter-agent communication protocols
- Action libraries for role-specific capabilities

## Project Structure

```
BLACKOUT/
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── agent_base.py          # Base agent class and interfaces
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── apex_agent.py          # APEX (CEO) agent
│   │   ├── conductor_agent.py     # CONDUCTOR (COO) agent
│   │   ├── vault_agent.py         # VAULT (CFO) agent
│   │   ├── oracle_agent.py        # ORACLE (Chief Strategy) agent
│   │   ├── forge_agent.py         # FORGE (CTO) agent
│   │   ├── vision_agent.py        # VISION (CPO) agent
│   │   ├── strike_agent.py        # STRIKE (CRO) agent
│   │   ├── shield_agent.py        # SHIELD (CISO) agent
│   │   └── architect_agent.py     # ARCHITECT (Engineering) agent
│   ├── departments/               # Department-specific agents (to be implemented)
│   └── utils/                     # Utility functions (to be implemented)
├── BLACKOUT_*_Charter.md         # Original documentation files
├── test_agents.py                 # Test script for agent framework
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Features

- **Agent Base Class**: Abstract base class defining common agent interface
- **Executive Agents**: Implementation of APEX, CONDUCTOR, VAULT, ORACLE, FORGE, VISION, STRIKE, SHIELD agents
- **Department Agents**: Starting with ARCHITECT from Engineering department
- **Decision Making**: Each agent implements documented decision frameworks
- **Action Libraries**: Role-specific actions for each agent type
- **Inter-Agent Communication**: Built-in messaging capabilities
- **State Management**: Agents maintain internal state and decision history
- **Extensible Design**: Easy to add new agent types and departments

## Installation

1. Clone or copy this repository
2. Ensure Python 3.8+ is installed
3. Install dependencies (optional for core framework):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Test Suite

```bash
python test_agents.py
```

This will create instances of all implemented agents and test their basic functionality.

### Creating Agents in Your Code

```python
from src.agents.apex_agent import ApexAgent
from src.agents.conductor_agent import ConductorAgent
# Import other agents as needed

# Create agent instances
apex = ApexAgent()
conductor = ConductorAgent()

# Check agent status
print(apex.get_status_summary())

# Make decisions
opportunity = {
    "id": "opp_001",
    "revenue_potential": 150000,
    "roi": 350,
    "aligns_with_strategy": True
}

decision = apex.evaluate_decision([opportunity])
print(f"Decision: {decision.decision.value}")
print(f"Rationale: {decision.rationale}")

# Agent-to-agent communication
apex.communicate("Strategic update", conductor)
```

## Agent Capabilities

Each agent type includes:
- Role-specific identity and authority level
- Documented decision-making framework
- Specialized action library
- Performance metrics and KPIs
- Communication capabilities
- State tracking and memory

## Extending the Framework

To add new agent types:
1. Create a new agent file in `src/agents/`
2. Inherit from `BlackoutAgent` in `src/core/agent_base.py`
3. Implement `_load_action_library()` and `_setup_decision_framework()`
4. Implement the `evaluate_decision()` method per the agent's decision framework
5. Add role-specific action methods

## Documentation

The original BLACKOUT documentation files are preserved in the root directory:
- `BLACKOUT_Agent_Framework.md` - Core agent architecture
- `BLACKOUT_Executive_Charter.md` - Executive leadership specifications
- `BLACKOUT_Engineering_Charter.md` - Engineering department details
- `BLACKOUT_Product_Charter.md` - Product department details
- `BLACKOUT_All_Departments_Summary.md` - Complete department overview
- `BLACKOUT_FACTORY_Launch.md` - Master launch document and roadmap

## License

This framework is provided as-is for educational and implementation purposes.

## Acknowledgments

Based on the BLACKOUT Factory concept and documentation provided.