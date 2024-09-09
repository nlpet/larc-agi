from abc import ABC, abstractmethod
from typing import List, Any


class BaseTask(ABC):
    def __init__(self, task_id: str):
        self.task_id = task_id

    @abstractmethod
    def generate(self) -> dict:
        """Generate the task content."""
        pass

    @abstractmethod
    def evaluate(self, response: Any) -> float:
        """Evaluate the response and return a score."""
        pass

    @abstractmethod
    def create_prompt(self) -> str:
        """Format the task as a prompt for the LLM."""
        pass

    @staticmethod
    @abstractmethod
    def parse_response(response: str) -> Any:
        """Parse the LLM's response."""
        pass
