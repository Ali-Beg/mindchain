# MindChain Agentic Framework

Welcome to the MindChain documentation!

## Overview

MindChain is a comprehensive framework for building, deploying, and managing AI agents with a unique Master Control Program (MCP) supervision layer. The architecture enables both simple single-agent workflows and complex multi-agent systems with advanced coordination capabilities.

## Current Implementation Status

MindChain is currently in its initial development phase with the following components implemented:

### Master Control Program (MCP)

The MCP serves as the supervisory layer of the system:

- **Agent Management**: Registration and unregistration of agents
- **Policy Enforcement**: Basic policies to control agent behavior
- **Resource Management**: Tracking and limiting resource usage
- **Execution Supervision**: Safe execution of agent tasks
- **Metrics Tracking**: Performance and usage statistics
- **Recovery System**: Basic error handling and agent reset capabilities

### Agent System

- **Agent Configuration**: Customizable agent parameters
- **Status Management**: Full agent lifecycle (initialization, idle, active, error states)
- **Basic Response Generation**: Simulated responses (LLM integration coming soon)
- **Tool Execution Interface**: Framework for adding tools to agents

### Memory System

- **Short-Term Memory**: Basic storage of recent interactions
- **Context Retrieval**: Simple retrieval of relevant previous information
- **Memory Management**: Operations to clear and maintain memory

## Getting Started

### Installation

MindChain is not yet published to PyPI. To use it:

1. Clone the repository
2. Install dependencies
3. Import from the src directory

### Basic Example

```python
import asyncio
from src.mindchain import MCP, Agent, AgentConfig

async def main():
    # Initialize the MCP
    mcp = MCP(config={
        'log_level': 'INFO',
        'policies': {
            'allow_external_tools': True,
        }
    })
    
    # Create agent configuration
    config = AgentConfig(
        name="AssistantAgent",
        description="General purpose assistant agent",
        system_prompt="You are a helpful AI assistant."
    )
    
    # Create and register an agent
    agent = Agent(config)
    agent_id = mcp.register_agent(agent)
    
    # Run the agent with MCP supervision
    response = await mcp.supervise_execution(
        agent_id=agent_id,
        task=lambda: agent.run("Hello! Can you introduce yourself?")
    )
    print(response)
    
    # Clean up
    mcp.unregister_agent(agent_id)

if __name__ == "__main__":
    asyncio.run(main())
```

## Demo Script

You can run the included demo script to see the framework in action:

```bash
python demo.py
```

This will demonstrate:
1. A single agent answering questions
2. A multi-agent workflow with specialized agents working together

## Testing

To verify the framework is working correctly:

```bash
python run_test.py
```

## Next Steps

The following features are planned for upcoming development:

1. **LLM Integration**: Connect to real language models
2. **Vector Database**: Enhanced memory with embeddings
3. **Tool Implementations**: Useful tools for agents
4. **Web Interface**: Visual monitoring and interaction
5. **Advanced Orchestration**: Sophisticated multi-agent coordination

## Project Structure

See the [Repository Structure](architecture/repository_structure.md) documentation for details on how the project is organized.
