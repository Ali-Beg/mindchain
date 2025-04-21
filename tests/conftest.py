"""
Test configuration for MindChain framework
"""
import pytest
import asyncio
import sys
import os
from typing import Dict, Any

# Import directly from src.mindchain which is cleaner
from src.mindchain import MCP, Agent, AgentConfig

@pytest.fixture
def test_config() -> Dict[str, Any]:
    """Provides a standard test configuration"""
    return {
        'log_level': 'WARNING',
        'policies': {
            'max_consecutive_errors': 3,
            'default_timeout': 5,
            'allow_external_tools': False,
        },
        'resource_limits': {
            'max_agents': 5,
            'max_tokens_per_request': 1000,
            'max_total_tokens': 10000,
        }
    }

@pytest.fixture
def mcp(test_config):
    """Provides a configured MCP instance for testing"""
    return MCP(config=test_config)

@pytest.fixture
def agent_config():
    """Provides a standard agent configuration for testing"""
    return AgentConfig(
        name="TestAgent",
        description="Agent for testing",
        model_name="test-model",
        system_prompt="You are a test agent.",
        temperature=0.0,  # Deterministic for testing
    )

@pytest.fixture
def agent(agent_config):
    """Provides a configured Agent instance for testing"""
    return Agent(agent_config)

@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for each test case"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
