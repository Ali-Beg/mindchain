"""
Test runner script with detailed error reporting
"""
import os
import sys
import traceback

def run_test():
    """Run tests with detailed error output"""
    print("Testing MindChain Framework...")
    print("==============================\n")
    
    try:
        # Import the key components first to check for import errors
        print("Verifying imports...")
        from src.mindchain import MCP, Agent, AgentConfig
        from src.mindchain.core.errors import MCPError
        print("✅ Basic imports successful\n")
        
        # Create test instances
        print("Creating test instances...")
        test_config = {
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
        
        mcp = MCP(config=test_config)
        print("✅ MCP instance created")
        
        agent_config = AgentConfig(
            name="TestAgent",
            description="Agent for testing",
            model_name="test-model",
            system_prompt="You are a test agent.",
        )
        agent = Agent(agent_config)
        print("✅ Agent instance created\n")
        
        # Run basic tests manually
        print("Running basic tests...")
        
        # Test 1: MCP Initialization
        print("Test 1: MCP Initialization")
        assert isinstance(mcp.agents, dict)
        assert len(mcp.agents) == 0
        print("✅ Passed\n")
        
        # Test 2: Agent Registration
        print("Test 2: Agent Registration")
        agent_id = mcp.register_agent(agent)
        assert agent_id in mcp.agents
        assert mcp.agents[agent_id] == agent
        print("✅ Passed\n")
        
        # Test 3: Agent Retrieval
        print("Test 3: Agent Retrieval")
        retrieved_agent = mcp.get_agent(agent_id)
        assert retrieved_agent == agent
        nonexistent = mcp.get_agent("nonexistent-id")
        assert nonexistent is None
        print("✅ Passed\n")
        
        # Test 4: Agent Unregistration
        print("Test 4: Agent Unregistration")
        success = mcp.unregister_agent(agent_id)
        assert success is True
        assert agent_id not in mcp.agents
        print("✅ Passed\n")
        
        # If we got here, basic functionality is working
        print("All basic tests passed successfully!")
        print("\nYour MindChain framework basic functionality is working correctly.")
        print("You can demonstrate this working code to your professor.")
        return 0
        
    except AssertionError as e:
        print(f"❌ Test failed: {str(e)}")
        traceback.print_exc()
        return 1
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("\nThis suggests there's an issue with your project structure or imports.")
        print("Make sure your package is properly installed or in the Python path.")
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(run_test())