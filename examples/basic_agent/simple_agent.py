"""
Simple Agent Example

This example demonstrates how to create a basic agent using the MindChain framework.
"""
import asyncio
import logging
from dotenv import load_dotenv

# Try to import from the installed package first, fall back to src.mindchain for local development
try:
    from mindchain import MCP, Agent, AgentConfig
except ImportError:
    from src.mindchain import MCP, Agent, AgentConfig

# Load environment variables from .env file (for future LLM API key)
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

async def main():
    # Initialize the Master Control Program (MCP)
    mcp = MCP(config={
        'log_level': 'INFO',
        'policies': {
            'allow_external_tools': True,
            'max_tokens_per_response': 2000,
        },
        'resource_limits': {
            'max_tokens_per_request': 2000,
            'max_agents': 5,
        }
    })
    
    # Create agent configuration
    config = AgentConfig(
        name="SimpleAssistant",
        description="A basic assistant agent",
        system_prompt="You are a helpful AI assistant that provides concise and accurate information."
    )
    
    # Create and register the agent
    agent = Agent(config)
    agent_id = mcp.register_agent(agent)
    
    print(f"Agent created with ID: {agent_id}")
    
    # Run the agent with a user query
    user_query = "Explain the concept of agentic AI in simple terms."
    
    print(f"\nUser: {user_query}\n")
    
    # Execute the query through MCP supervision
    response = await mcp.supervise_execution(
        agent_id=agent_id,
        task=lambda: agent.run(user_query)
    )
    
    print(f"Agent: {response}\n")
    
    # Ask a follow-up question
    follow_up = "What are the key components needed to build an effective AI agent?"
    
    print(f"User: {follow_up}\n")
    
    response = await mcp.supervise_execution(
        agent_id=agent_id,
        task=lambda: agent.run(follow_up)
    )
    
    print(f"Agent: {response}")
    
    # Unregister the agent when done
    mcp.unregister_agent(agent_id)
    print("\nAgent unregistered")

if __name__ == "__main__":
    asyncio.run(main())
