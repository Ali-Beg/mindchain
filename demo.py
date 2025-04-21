"""
MindChain Demo Script

This script demonstrates the core functionality of the MindChain framework.
Run this script to see the framework in action.
"""
import asyncio
import logging
import time
from typing import Dict, Any

from src.mindchain import MCP, Agent, AgentConfig, AgentStatus, MemoryManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("MindChainDemo")

async def simulate_agent_response(agent_name: str, query: str) -> str:
    """
    Simulate an agent's response to a query without using an actual LLM API.
    
    Args:
        agent_name: Name of the agent
        query: User query
        
    Returns:
        str: Simulated response
    """
    # Simulate thinking time
    await asyncio.sleep(1)
    
    # Generate deterministic responses based on query
    if "introduction" in query.lower() or "hello" in query.lower():
        return f"Hello! I'm {agent_name}, an AI assistant built with the MindChain framework. I can help answer questions and solve problems."
    
    elif "framework" in query.lower() or "mindchain" in query.lower():
        return (f"MindChain is an agentic AI framework with a unique Master Control Program (MCP) supervision layer. "
                f"It enables both simple single-agent workflows and complex multi-agent systems with advanced coordination capabilities.")
    
    elif "capabilities" in query.lower() or "what can you do" in query.lower():
        return (f"As {agent_name}, I can demonstrate the core capabilities of the MindChain framework, such as:\n"
                f"1. Agent management through the MCP\n"
                f"2. Policy enforcement\n"
                f"3. Memory management\n"
                f"4. Resource monitoring\n"
                f"5. Multi-agent coordination")
    
    else:
        return (f"I understand you're asking about '{query}'. As a simulated agent in this demo, "
                f"I have limited responses. But in a full implementation, I would use an LLM to generate "
                f"meaningful responses to your query.")

async def run_simple_agent_demo():
    """Run a simple demonstration with one agent"""
    print("\n" + "="*50)
    print("MINDCHAIN FRAMEWORK DEMONSTRATION")
    print("="*50 + "\n")
    
    print("Initializing Master Control Program (MCP)...")
    mcp = MCP(config={
        'log_level': 'INFO',
        'policies': {
            'allow_external_tools': True,
            'max_tokens_per_response': 2000,
        }
    })
    print("✅ MCP initialized successfully\n")
    
    print("Creating and registering an agent...")
    agent_config = AgentConfig(
        name="DemoAssistant",
        description="A demonstration assistant agent",
        model_name="gpt-4",  # This is just for demonstration, no real API calls are made
        system_prompt="You are a helpful AI assistant built with the MindChain framework.",
    )
    
    # Create the agent
    agent = Agent(agent_config)
    
    # Patch the _generate_response method to use our simulation
    original_generate_response = agent._generate_response
    agent._generate_response = lambda query, context: simulate_agent_response(agent.name, query)
    
    # Register with MCP
    agent_id = mcp.register_agent(agent)
    print(f"✅ Agent '{agent.name}' created with ID: {agent_id}\n")
    
    # Get system status
    print("Checking MCP system status...")
    status = mcp.get_system_status()
    print(f"- Total agents: {status['total_agents']}")
    print(f"- Agent statuses: {status['agent_status']}")
    print(f"- System uptime: {status['uptime']:.2f} seconds\n")
    
    # List registered agents
    print("Listing registered agents:")
    agents = mcp.list_agents()
    for idx, agent_info in enumerate(agents, 1):
        print(f"  {idx}. {agent_info['name']} (ID: {agent_info['id']})")
    print()
    
    # Run a few queries
    queries = [
        "Hello! Can you introduce yourself?",
        "Tell me about the MindChain framework.",
        "What are your capabilities?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"Query {i}: {query}")
        
        # Execute through MCP supervision
        print("Agent is thinking...")
        start_time = time.time()
        
        response = await mcp.supervise_execution(
            agent_id=agent_id,
            task=lambda: agent.run(query)
        )
        
        elapsed = time.time() - start_time
        print(f"Response (took {elapsed:.2f}s):\n{response}\n")
        
        # Wait a bit between queries
        if i < len(queries):
            await asyncio.sleep(0.5)
    
    # Show metrics
    metrics = mcp.agent_metrics[agent_id]
    print("\nAgent metrics:")
    print(f"- Total tasks completed: {metrics.total_tasks_completed}")
    print(f"- Average response time: {metrics.average_response_time:.2f} seconds")
    print(f"- Total errors: {metrics.total_errors}")
    
    # Unregister the agent
    mcp.unregister_agent(agent_id)
    print("\n✅ Agent unregistered")
    print("\nDemo completed successfully!")

async def run_multi_agent_demo():
    """Run a demonstration with multiple agents working together"""
    print("\n" + "="*50)
    print("MINDCHAIN MULTI-AGENT DEMONSTRATION")
    print("="*50 + "\n")
    
    print("Initializing Master Control Program (MCP)...")
    mcp = MCP(config={
        'log_level': 'INFO',
        'policies': {
            'allow_external_tools': True,
        }
    })
    print("✅ MCP initialized successfully\n")
    
    print("Creating a team of specialized agents...")
    
    # Create agent configurations
    agent_configs = [
        AgentConfig(
            name="ResearchAgent",
            description="Specializes in finding and synthesizing information",
            system_prompt="You are a research agent that finds and synthesizes information."
        ),
        AgentConfig(
            name="AnalysisAgent",
            description="Specializes in analyzing information and extracting insights",
            system_prompt="You are an analysis agent that examines information critically."
        ),
        AgentConfig(
            name="WritingAgent",
            description="Specializes in creating well-written content",
            system_prompt="You are a writing agent that creates clear and engaging content."
        )
    ]
    
    # Create and register agents
    agents = []
    agent_ids = []
    
    for config in agent_configs:
        agent = Agent(config)
        
        # Patch _generate_response to use our simulation
        agent._generate_response = lambda query, context: simulate_agent_response(agent.name, query)
        
        agent_id = mcp.register_agent(agent)
        agents.append(agent)
        agent_ids.append(agent_id)
        print(f"✅ Agent '{agent.name}' created with ID: {agent_id}")
    
    print("\nAll agents registered successfully!\n")
    
    # Demonstrate multi-agent workflow
    print("Demonstrating a multi-agent workflow for content creation:")
    print("1. Research Agent → 2. Analysis Agent → 3. Writing Agent\n")
    
    # The topic to process through the workflow
    topic = "The impact of agentic AI frameworks on software development"
    print(f"Topic: \"{topic}\"\n")
    
    # Step 1: Research phase
    print("Step 1: Research Agent gathering information...")
    research_prompt = f"Research the following topic and provide key facts and information: {topic}"
    
    research_result = await mcp.supervise_execution(
        agent_id=agent_ids[0],
        task=lambda: agents[0].run(research_prompt)
    )
    
    print(f"Research Agent result:\n{research_result}\n")
    
    # Step 2: Analysis phase
    print("Step 2: Analysis Agent examining research findings...")
    analysis_prompt = f"Analyze this research and extract key insights:\n\n{research_result}"
    
    analysis_result = await mcp.supervise_execution(
        agent_id=agent_ids[1],
        task=lambda: agents[1].run(analysis_prompt)
    )
    
    print(f"Analysis Agent result:\n{analysis_result}\n")
    
    # Step 3: Writing phase
    print("Step 3: Writing Agent creating final content...")
    writing_prompt = f"Create a well-structured article on '{topic}' based on this research and analysis:\n\nResearch:\n{research_result}\n\nAnalysis:\n{analysis_result}"
    
    final_content = await mcp.supervise_execution(
        agent_id=agent_ids[2],
        task=lambda: agents[2].run(writing_prompt)
    )
    
    print(f"Writing Agent result (final output):\n{final_content}\n")
    
    # Show MCP status after the workflow
    print("Final MCP system status:")
    status = mcp.get_system_status()
    print(f"- Total agents: {status['total_agents']}")
    print(f"- Total tasks completed: {status['total_tasks_completed']}")
    
    # Unregister all agents
    for agent_id in agent_ids:
        mcp.unregister_agent(agent_id)
    
    print("\n✅ All agents unregistered")
    print("Multi-agent demo completed successfully!")

async def main():
    """Run all demonstrations"""
    await run_simple_agent_demo()
    print("\nPreparing for multi-agent demo...\n")
    await asyncio.sleep(2)  # Short pause between demos
    await run_multi_agent_demo()

if __name__ == "__main__":
    asyncio.run(main())