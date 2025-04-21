"""
Basic unit tests for the Agent class.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from mindchain import Agent, AgentConfig

class TestAgentBasic:
    """Basic tests for Agent class functionality."""
    
    def test_agent_initialization(self):
        """Test that an agent can be properly initialized."""
        config = AgentConfig(
            name="TestAgent",
            description="Test agent",
            system_prompt="You are a test agent."
        )
        
        agent = Agent(config)
        
        assert agent.name == "TestAgent"
        assert agent.config.description == "Test agent"
        assert agent.config.system_prompt == "You are a test agent."
    
    def test_agent_reset(self):
        """Test that agent reset clears state properly."""
        config = AgentConfig(name="TestAgent")
        agent = Agent(config)
        
        # Set some state
        agent._history = ["some history"]
        agent._last_response = "last response"
        agent.current_task = "current task"
        
        # Reset agent
        agent.reset()
        
        # Check state is cleared
        assert agent._history == []
        assert agent._last_response is None
        assert agent.current_task is None
    
    def test_add_and_remove_tool(self):
        """Test that tools can be added and removed."""
        config = AgentConfig(name="TestAgent")
        agent = Agent(config)
        
        # Define a simple tool function
        def dummy_tool():
            return "tool result"
        
        # Add the tool
        agent.add_tool("dummy_tool", dummy_tool)
        assert "dummy_tool" in agent.tools
        assert agent.tools["dummy_tool"] is dummy_tool
        
        # Remove the tool
        result = agent.remove_tool("dummy_tool")
        assert result is True
        assert "dummy_tool" not in agent.tools
        
        # Try to remove non-existent tool
        result = agent.remove_tool("nonexistent_tool")
        assert result is False
    
    @pytest.mark.asyncio
    @patch("mindchain.core.agent.Agent._generate_response")
    async def test_agent_run(self, mock_generate_response):
        """Test that agent can run with a user input."""
        # Configure mock
        mock_response = "This is a test response"
        mock_generate_response.return_value = mock_response
        
        # Create agent
        config = AgentConfig(name="TestAgent")
        agent = Agent(config)
        
        # Mock memory methods
        agent.memory = AsyncMock()
        agent.memory.retrieve_relevant.return_value = []
        agent.memory.store = AsyncMock()
        
        # Run agent
        response = await agent.run("Test input")
        
        # Assertions
        assert response == mock_response
        assert agent._last_response == mock_response
        assert len(agent._history) == 2
        assert agent._history[0]["role"] == "user"
        assert agent._history[0]["content"] == "Test input"
        assert agent._history[1]["role"] == "assistant"
        assert agent._history[1]["content"] == mock_response
