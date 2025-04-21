"""
Multi-Agent Collaboration Example

This example demonstrates how to create a team of agents that work together to solve a problem
using the AgentOrchestrator to manage the workflow.
"""
import asyncio
import logging
from typing import Dict, List, Any
from dotenv import load_dotenv

# Update import path to match the current implementation
from src.mindchain import MCP, Agent, AgentConfig
from src.mindchain.core.orchestrator import AgentOrchestrator

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
        },
        'resource_limits': {
            'max_tokens_per_request': 2000,
        }
    })
    
    # Create an orchestrator for managing the agent team
    orchestrator = AgentOrchestrator(mcp)
    
    # Define our team of agents
    agent_configs = [
        AgentConfig(
            name="Researcher",
            description="Researches information and finds relevant data",
            system_prompt=(
                "You are a research agent specializing in finding and synthesizing information. "
                "Your goal is to discover relevant facts and data about the given topic."
            )
        ),
        AgentConfig(
            name="Analyst",
            description="Analyzes information and extracts insights",
            system_prompt=(
                "You are an analytical agent that excels at examining information critically. "
                "Your goal is to analyze data, identify patterns, and extract valuable insights."
            )
        ),
        AgentConfig(
            name="Writer",
            description="Creates well-written content based on provided information",
            system_prompt=(
                "You are a writing agent skilled in creating clear and engaging content. "
                "Your goal is to take information and insights and produce well-organized written materials."
            )
        )
    ]
    
    # Create and register the team
    agent_ids = []
    for config in agent_configs:
        agent = Agent(config)
        agent_id = mcp.register_agent(agent)
        agent_ids.append(agent_id)
        print(f"Registered agent '{config.name}' with ID: {agent_id}")
    
    # The topic we want our team to collaborate on
    topic = "The impact of artificial intelligence on future job markets"
    print(f"\nTeam Collaboration Topic: {topic}\n")
    
    # Create a sequential workflow for the collaborative task
    workflow_id = orchestrator.create_sequential_workflow(
        name="Research and Article Creation",
        description=f"Research and create an article about: {topic}",
        agent_ids=agent_ids,
        prompts=[
            f"Research the following topic and provide key facts and information: {topic}",
            "Analyze the following research information and extract key insights:\n\n{previous_result}",
            "Create a well-structured short article based on this research and analysis:\n\nResearch:\n{previous_result}"
        ]
    )
    
    print(f"Created workflow with ID: {workflow_id}")
    print("Starting workflow execution...")
    
    # Execute the workflow and get results
    try:
        results = await orchestrator.execute_workflow(workflow_id)
        
        # Get the final article from the last step
        workflow = orchestrator.get_workflow(workflow_id)
        final_step_id = workflow['steps'][-1]['id']
        final_article = results[final_step_id]
        
        print("\n=== FINAL ARTICLE ===\n")
        print(final_article)
        
    except Exception as e:
        print(f"Error executing workflow: {e}")
    
    # Clean up
    for agent_id in agent_ids:
        mcp.unregister_agent(agent_id)
    print("\nAll agents unregistered")

if __name__ == "__main__":
    asyncio.run(main())
