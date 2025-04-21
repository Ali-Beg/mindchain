"""
Unit tests for the Master Control Program (MCP)
"""
import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch

# Try to import from the installed package first, fall back to src.mindchain for local development
try:
    from mindchain import MCP, Agent
    from mindchain.core.errors import MCPError
except ImportError:
    from src.mindchain import MCP, Agent
    from src.mindchain.core.errors import MCPError

class TestMCP:
    """Test cases for the MCP class"""
    
    def test_init(self, test_config):
        """Test MCP initialization"""
        mcp = MCP(config=test_config)
        assert mcp.config == test_config
        assert isinstance(mcp.agents, dict)
        assert len(mcp.agents) == 0
        
    def test_register_agent(self, mcp, agent):
        """Test registering an agent with MCP"""
        agent_id = mcp.register_agent(agent)
        assert agent_id in mcp.agents
        assert mcp.agents[agent_id] == agent
        assert agent_id in mcp.agent_metrics
        
    def test_register_agent_with_max_reached(self, test_config, agent):
        """Test registering agent when max limit is reached"""
        # Set max_agents to 0 for testing
        test_config['resource_limits']['max_agents'] = 0
        mcp = MCP(config=test_config)
        
        with pytest.raises(MCPError, match="Maximum number of agents reached"):
            mcp.register_agent(agent)
            
    def test_unregister_agent(self, mcp, agent):
        """Test unregistering an agent from MCP"""
        agent_id = mcp.register_agent(agent)
        assert agent_id in mcp.agents
        
        success = mcp.unregister_agent(agent_id)
        assert success is True
        assert agent_id not in mcp.agents
        assert agent_id not in mcp.agent_metrics
        
    def test_unregister_nonexistent_agent(self, mcp):
        """Test unregistering an agent that doesn't exist"""
        success = mcp.unregister_agent("nonexistent-id")
        assert success is False
        
    def test_get_agent(self, mcp, agent):
        """Test getting an agent by ID"""
        agent_id = mcp.register_agent(agent)
        retrieved_agent = mcp.get_agent(agent_id)
        assert retrieved_agent == agent
        
        nonexistent = mcp.get_agent("nonexistent-id")
        assert nonexistent is None
        
    def test_list_agents(self, mcp, agent):
        """Test listing all registered agents"""
        agent_id = mcp.register_agent(agent)
        agents_list = mcp.list_agents()
        
        assert len(agents_list) == 1
        assert agents_list[0]['id'] == agent_id
        assert agents_list[0]['name'] == agent.name
        
    def test_update_metrics(self, mcp, agent):
        """Test updating agent metrics"""
        agent_id = mcp.register_agent(agent)
        
        # Initial values
        metrics = mcp.agent_metrics[agent_id]
        assert metrics.total_tokens_used == 0
        assert metrics.total_api_calls == 0
        assert metrics.total_tasks_completed == 0
        assert metrics.total_errors == 0
        
        # Update metrics
        mcp.update_metrics(
            agent_id=agent_id,
            tokens_used=100,
            api_calls=2,
            task_completed=True,
            error_occurred=False,
            response_time=0.5
        )
        
        # Check updated values
        metrics = mcp.agent_metrics[agent_id]
        assert metrics.total_tokens_used == 100
        assert metrics.total_api_calls == 2
        assert metrics.total_tasks_completed == 1
        assert metrics.total_errors == 0
        assert metrics.average_response_time == 0.5
        
    @pytest.mark.asyncio
    async def test_supervise_execution(self, mcp, agent):
        """Test supervising task execution"""
        agent_id = mcp.register_agent(agent)
        
        # Use AsyncMock instead of MagicMock to return a coroutine
        mock_task = AsyncMock(return_value="Task result")
        
        result = await mcp.supervise_execution(agent_id, mock_task)
        assert result == "Task result"
        mock_task.assert_called_once()
        
    @pytest.mark.asyncio
    async def test_supervise_execution_error(self, mcp, agent):
        """Test supervising task execution with error"""
        agent_id = mcp.register_agent(agent)
        
        # Use AsyncMock for async errors too
        mock_task = AsyncMock(side_effect=ValueError("Test error"))
        
        with pytest.raises(ValueError, match="Test error"):
            await mcp.supervise_execution(agent_id, mock_task)
