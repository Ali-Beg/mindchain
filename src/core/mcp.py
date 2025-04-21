"""
Master Control Program (MCP)

The supervisory layer responsible for managing and monitoring all agents in the system.
"""
import logging
import uuid
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Callable, TypeVar, cast

from .agent import Agent
from .errors import MCPError

logger = logging.getLogger(__name__)

T = TypeVar('T')

@dataclass
class AgentMetrics:
    """Metrics for tracking agent performance and resource usage"""
    created_at: float
    last_active: float
    total_tokens_used: int = 0
    total_api_calls: int = 0
    total_tasks_completed: int = 0
    total_errors: int = 0
    average_response_time: float = 0.0


class MCP:
    """
    Master Control Program - Supervisory layer for the agent system
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the MCP with the given configuration
        
        Args:
            config: Configuration parameters for the MCP
        """
        self.config = config or {}
        self.agents: Dict[str, Agent] = {}
        self.agent_metrics: Dict[str, AgentMetrics] = {}
        self.policies = self._load_policies()
        self.resource_limits = self._load_resource_limits()
        self._init_logging()
        logger.info("Master Control Program initialized")
    
    def _init_logging(self) -> None:
        """Configure logging system based on configuration"""
        log_level = self.config.get('log_level', 'INFO')
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        )
    
    def _load_policies(self) -> Dict[str, Any]:
        """Load policy definitions from configuration"""
        policies: Dict[str, Any] = self.config.get('policies', {
            'max_consecutive_errors': 3,
            'default_timeout': 30,
            'allow_external_tools': False,
        })
        return policies
    
    def _load_resource_limits(self) -> Dict[str, Any]:
        """Load resource limit definitions from configuration"""
        resource_limits: Dict[str, Any] = self.config.get('resource_limits', {
            'max_agents': 10,
            'max_tokens_per_request': 4000,
            'max_total_tokens': 100000,
            'max_concurrent_tasks': 5,
        })
        return resource_limits
    
    def register_agent(self, agent: Agent) -> str:
        """
        Register an agent with MCP for supervision
        
        Args:
            agent: The agent instance to register
            
        Returns:
            agent_id: Unique ID assigned to the agent
        """
        # Check if we've reached the maximum number of agents
        if len(self.agents) >= self.resource_limits.get('max_agents'):
            raise MCPError("Maximum number of agents reached")
        
        # Generate a unique ID for the agent if not already set
        agent_id = agent.id if hasattr(agent, 'id') and agent.id else str(uuid.uuid4())
        agent.id = agent_id
        
        # Store the agent and initialize its metrics
        self.agents[agent_id] = agent
        self.agent_metrics[agent_id] = AgentMetrics(
            created_at=time.time(),
            last_active=time.time()
        )
        
        logger.info(f"Agent registered with ID: {agent_id}")
        return agent_id
    
    def unregister_agent(self, agent_id: str) -> bool:
        """
        Unregister an agent from MCP supervision
        
        Args:
            agent_id: The unique ID of the agent to unregister
            
        Returns:
            success: Whether the agent was successfully unregistered
        """
        if agent_id in self.agents:
            # Perform cleanup for the agent
            agent = self.agents.pop(agent_id)
            self.agent_metrics.pop(agent_id, None)
            logger.info(f"Agent {agent_id} unregistered")
            return True
        return False
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """
        Get an agent by its ID
        
        Args:
            agent_id: The agent's unique identifier
            
        Returns:
            agent: The agent instance if found, None otherwise
        """
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """
        List all registered agents with their basic information
        
        Returns:
            agents_info: List of agent information dictionaries
        """
        return [
            {
                'id': agent_id,
                'name': agent.name,
                'status': agent.status,
                'created_at': self.agent_metrics[agent_id].created_at,
                'last_active': self.agent_metrics[agent_id].last_active,
            }
            for agent_id, agent in self.agents.items()
        ]
    
    def update_metrics(self, agent_id: str, 
                      tokens_used: int = 0, 
                      api_calls: int = 0,
                      task_completed: bool = False,
                      error_occurred: bool = False,
                      response_time: Optional[float] = None) -> None:
        """
        Update the metrics for an agent
        
        Args:
            agent_id: The agent's unique identifier
            tokens_used: Number of tokens used in this operation
            api_calls: Number of API calls made in this operation
            task_completed: Whether a task was completed
            error_occurred: Whether an error occurred
            response_time: Time taken to generate a response (in seconds)
        """
        if agent_id not in self.agent_metrics:
            logger.warning(f"Attempted to update metrics for unregistered agent {agent_id}")
            return
        
        metrics = self.agent_metrics[agent_id]
        metrics.last_active = time.time()
        metrics.total_tokens_used += tokens_used
        metrics.total_api_calls += api_calls
        
        if task_completed:
            metrics.total_tasks_completed += 1
        
        if error_occurred:
            metrics.total_errors += 1
        
        if response_time is not None:
            # Update running average
            if metrics.average_response_time == 0:
                metrics.average_response_time = response_time
            else:
                # Simple moving average
                metrics.average_response_time = (metrics.average_response_time * 0.9) + (response_time * 0.1)
    
    def check_policy_compliance(self, agent: Agent, action: str, 
                              parameters: Dict[str, Any]) -> bool:
        """
        Check if an agent action complies with system policies
        
        Args:
            agent: The agent attempting the action
            action: The action the agent is attempting
            parameters: Parameters of the action
            
        Returns:
            compliant: Whether the action complies with policies
        """
        # Example policy checks
        if action == "execute_tool":
            tool_name = parameters.get("tool_name", "")
            
            # Check if external tools are allowed
            if not self.policies.get("allow_external_tools", False) and \
               tool_name in ["web_search", "code_execution"]:
                logger.warning(f"Agent {agent.id} attempted to use restricted tool: {tool_name}")
                return False
        
        # Check for rate limiting based on agent metrics
        metrics = self.agent_metrics.get(agent.id)
        if metrics:
            # Check if agent has exceeded token limits
            if metrics.total_tokens_used > self.resource_limits.get("max_total_tokens", float('inf')):
                logger.warning(f"Agent {agent.id} exceeded total token limit")
                return False
        
        return True
    
    def supervise_execution(self, agent_id: str, task: Callable[[], T], 
                          timeout: Optional[float] = None) -> T:
        """
        Supervise the execution of a task by an agent
        
        Args:
            agent_id: The agent's unique identifier
            task: The task function to execute
            timeout: Maximum time allowed for execution (seconds)
            
        Returns:
            result: The result of the task execution
        """
        if agent_id not in self.agents:
            raise MCPError(f"Unknown agent ID: {agent_id}")
        
        agent = self.agents[agent_id]
        task_timeout = timeout or self.policies.get("default_timeout", 30)
        
        start_time = time.time()
        try:
            # Track that the agent is active
            self.agent_metrics[agent_id].last_active = start_time
            
            # Execute the task with timeout
            # Note: In a real implementation, you would use async/await or threading
            # for proper timeout handling. This is simplified for illustration.
            result = task()
            
            # Update metrics
            elapsed = time.time() - start_time
            self.update_metrics(
                agent_id=agent_id,
                task_completed=True,
                response_time=elapsed
            )
            
            return result
            
        except Exception as e:
            # Update error metrics
            self.update_metrics(
                agent_id=agent_id,
                error_occurred=True
            )
            
            logger.error(f"Agent {agent_id} execution error: {str(e)}")
            raise
    
    def recover_agent(self, agent_id: str) -> bool:
        """
        Attempt to recover an agent that's in an error state
        
        Args:
            agent_id: The agent's unique identifier
            
        Returns:
            success: Whether recovery was successful
        """
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        logger.info(f"Attempting to recover agent {agent_id}")
        
        # Example recovery logic - reset agent state
        try:
            agent.reset()
            return True
        except Exception as e:
            logger.error(f"Failed to recover agent {agent_id}: {str(e)}")
            return False
            
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get the overall status of the MCP system
        
        Returns:
            status: Dictionary containing system status information
        """
        active_agents = sum(1 for a in self.agents.values() if a.status == "active")
        total_tokens = sum(m.total_tokens_used for m in self.agent_metrics.values())
        total_tasks = sum(m.total_tasks_completed for m in self.agent_metrics.values())
        total_errors = sum(m.total_errors for m in self.agent_metrics.values())
        
        return {
            "total_agents": len(self.agents),
            "active_agents": active_agents,
            "total_tokens_used": total_tokens,
            "total_tasks_completed": total_tasks,
            "total_errors": total_errors,
            "uptime": time.time() - min(m.created_at for m in self.agent_metrics.values()) if self.agent_metrics else 0,
        }
