# MindChain Repository Structure

This document provides an architectural overview of the current MindChain repository structure.

## Directory Structure

```
mindchain/
├── docs/                              # Documentation
│   ├── architecture/                  # Architecture documentation
│   │   └── repository_structure.md    # This file
│   ├── index.md                       # Main documentation page
│   └── mkdocs.yml                     # MkDocs configuration
│
├── examples/                          # Example code
│   ├── basic_agent/                   # Basic agent examples
│   │   └── simple_agent.py            # Simple agent example
│   └── multi_agent/                   # Multi-agent examples
│       └── team_collaboration.py      # Team collaboration example
│
├── src/                               # Source code
│   ├── core/                          # Legacy core module (being migrated)
│   │   ├── __init__.py                # Core package initialization
│   │   ├── errors.py                  # Error definitions
│   │   └── mcp.py                     # Original MCP implementation
│   │
│   └── mindchain/                     # Main package
│       ├── __init__.py                # Package initialization
│       ├── cli.py                     # Command line interface
│       │
│       ├── core/                      # Core components
│       │   ├── __init__.py            # Core package initialization
│       │   ├── agent.py               # Agent implementation
│       │   └── errors.py              # Error definitions
│       │
│       ├── mcp/                       # Master Control Program
│       │   ├── __init__.py            # MCP package initialization  
│       │   ├── mcp.py                 # MCP implementation
│       │   ├── policies.py            # Policy management
│       │   ├── resource_manager.py    # Resource management
│       │   └── metrics.py             # Agent metrics tracking
│       │
│       ├── memory/                    # Memory systems
│       │   ├── __init__.py            # Memory package initialization
│       │   └── memory_manager.py      # Basic memory manager
│       │
│       └── tools/                     # Tool implementations (placeholder)
│           └── __init__.py            # Tools package initialization
│
├── tests/                             # Tests
│   ├── unit/                          # Unit tests
│   │   ├── test_mcp.py                # MCP tests
│   │   └── test_agent_basic.py        # Basic agent tests
│   └── conftest.py                    # Test configurations and fixtures
│
├── demo.py                            # Demonstration script
├── run_test.py                        # Test runner script
├── CODE_OF_CONDUCT.md                 # Code of conduct
├── CONTRIBUTING.md                    # Contributing guidelines
├── LICENSE                            # Project license
├── README.md                          # Project overview
├── ROADMAP.md                         # Project roadmap
├── SECURITY.md                        # Security policy
└── pyproject.toml                     # Project configuration
```

## Component Architecture

The current implementation includes the following key components:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                 ┌─────────────────────────┐                     │
│                 │                         │                     │
│                 │     Master Control      │                     │
│                 │     Program (MCP)       │                     │
│                 │                         │                     │
│                 └───────────┬─────────────┘                     │
│                             │                                   │
│                             │ manages                           │
│                             ▼                                   │
│     ┌───────────┐     ┌───────────┐     ┌───────────┐          │
│     │           │     │           │     │           │          │
│     │  Agent 1  │     │  Agent 2  │     │  Agent 3  │          │
│     │           │     │           │     │           │          │
│     └─────┬─────┘     └─────┬─────┘     └─────┬─────┘          │
│           │                 │                 │                 │
│           │                 │                 │                 │
│     ┌─────▼─────┐                                              │
│     │           │                                              │
│     │  Memory   │                                              │
│     │           │                                              │
│     └───────────┘                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Key Components

### Master Control Program (MCP)

The MCP serves as the central supervisory system with these implemented capabilities:

- Agent lifecycle management (registration, unregistration)
- Policy enforcement through the PolicyManager
- Resource allocation and monitoring via ResourceManager
- Metrics tracking for agent performance
- Supervised execution of agent tasks

### Agents

Agents have been implemented with these features:
- Configuration via AgentConfig
- Status management (INITIALIZING, IDLE, ACTIVE, etc.)
- Basic response generation (placeholder for LLM integration)
- Simple memory interaction
- Tool execution interface (framework for future tool implementations)

### Memory System

The current memory implementation includes:
- Simple memory manager with short-term storage
- Basic memory retrieval for context
- Memory clearing operations

### Policies

The policy system currently implements:
- Safety controls for agent behavior
- Token limit enforcement
- Tool permission management

### Resource Management

Resource management features include:
- Token usage tracking
- Agent allocation limits
- Task execution controls
- API rate limiting

## Current Implementation Status

The current implementation provides:

1. A working framework for agent supervision via MCP
2. Basic agent functionality with simulated responses
3. Simple memory management
4. Policy enforcement mechanisms
5. Resource tracking and limits

This represents the initial implementation phase, focusing on the architectural foundation and core supervision capabilities. The next development phases will expand functionality with:

1. Real LLM integration
2. Advanced memory with vector storage
3. Tool implementations
4. Planning and orchestration systems

## Demo and Testing

The current implementation includes:
- A demonstration script (demo.py) showing both single-agent and multi-agent capabilities
- Basic tests verifying core functionality
- A test helper script (run_test.py) to validate the implementation
