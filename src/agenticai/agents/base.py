"""Base agent classes."""
from dataclasses import dataclass
# Replace actual crewai import with a mock implementation
# from crewai import Agent

@dataclass
class AgentConfig:
    """Configuration for an agent."""
    name: str
    role: str
    goal: str
    backstory: str = ""
    temperature: float = 0.7
    verbose: bool = False
    llm_config: dict = None
    tools: list = None
    
    def to_dict(self):
        """Convert config to dictionary."""
        return {
            "name": self.name,
            "role": self.role,
            "goal": self.goal,
            "backstory": self.backstory,
            "temperature": self.temperature,
            "verbose": self.verbose,
            "llm_config": self.llm_config,
            "tools": self.tools
        }

# Create a mock Agent class to replace the crewAI one
class Agent:
    """Mock crewAI Agent class."""
    def __init__(self, name, role, goal, backstory="", verbose=False, allow_delegation=True, 
                 tools=None, max_iter=15, max_rpm=None, max_tokens=None, memory=True,
                 temperature=0.7, callbacks=None, llm=None, **kwargs):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.verbose = verbose
        self.allow_delegation = allow_delegation
        self.tools = tools or []
        self.max_iter = max_iter
        self.max_rpm = max_rpm
        self.max_tokens = max_tokens
        self.memory = memory
        self.temperature = temperature
        self.callbacks = callbacks
        self.llm = llm
        self.kwargs = kwargs

class BaseAgent:
    """Base agent class with common functionality."""
    
    def __init__(self, config: AgentConfig = None):
        """Initialize the agent with configuration."""
        self.config = config or AgentConfig(
            name="BaseAgent",
            role="Generic Agent",
            goal="Perform tasks as assigned",
        )
        
        # Create a crewAI agent with the configuration
        self.agent = Agent(
            name=self.config.name,
            role=self.config.role,
            goal=self.config.goal,
            backstory=self.config.backstory,
            verbose=self.config.verbose,
            temperature=self.config.temperature,
            tools=self.config.tools or [],
        )
        
    async def execute(self, task_description: str, context: dict = None) -> dict:
        """Execute a task with the agent (async interface)."""
        # In a real implementation, this would call the crewAI agent
        # For now, just return a mock response
        return {
            "result": f"Executed '{task_description}' with agent {self.config.name}",
            "agent": self.config.name,
            "task": task_description,
            "context": context or {},
        }
