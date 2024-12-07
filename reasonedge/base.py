from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
import time

class BaseReasoner(ABC):
    """
    Abstract base class for reasoning algorithms.
    All reasoning implementations should inherit from this class.
    This class provides a template for reasoning processes, ensuring
    consistency and standardization across different reasoning models.
    """

    def __init__(self, model_name: str, temperature: float = 1.0, **kwargs):
        """
        Initialize the base reasoner with a specified model and parameters.
        
        Args:
            model_name (str): The name of the language model to be used.
            temperature (float): The temperature setting for the model, affecting randomness.
            **kwargs: Additional keyword arguments for specific implementations.
        """
        self.model_name = model_name
        self.temperature = temperature
        self.kwargs = kwargs

    @abstractmethod
    def reason(self, 
               prompt: str,
               context: Optional[Union[str, List[str]]] = None,
               **kwargs) -> Dict[str, Any]:
        """
        Main reasoning method that must be implemented by all subclasses.
        This method processes the input prompt and context to generate a reasoned response.
        
        Args:
            prompt (str): The input prompt/question to reason about.
            context (Optional[Union[str, List[str]]]): Additional context for reasoning.
            **kwargs: Additional keyword arguments for specific implementations.
            
        Returns:
            Dict[str, Any]: A dictionary containing at least:
                - 'response': The final reasoned response.
                - 'reasoning_steps': List of intermediate reasoning steps.
                - 'confidence': Confidence score of the response (0-1).
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def format_response(self, 
                        response: str, 
                        reasoning_steps: List[str], 
                        final_answer: str, 
                        start_time: float,
                        temperature: float) -> Dict[str, Any]:
        """
        Format the reasoning response into a standardized structure.
        Can be overridden by subclasses for custom formatting.
        
        Args:
            response (str): The raw response from the reasoning process.
            reasoning_steps (List[str]): The steps taken during reasoning.
            final_answer (str): The final answer derived from the reasoning process.
            start_time (float): The timestamp when the reasoning process started.
            temperature (float): The temperature setting used during reasoning.
            
        Returns:
            Dict[str, Any]: Formatted response dictionary including execution time and metadata.
        """
        return {
            'response': response,
            'reasoning_steps': reasoning_steps,
            'final_answer': final_answer,
            'execution_time': time.time() - start_time,
            'metadata': {
                'model_name': self.model_name,
                'temperature': temperature
            }
        }

    def _extract_reasoning_steps(self, response: str) -> List[str]:
        """
        Abstract method to extract reasoning steps from a response.
        Subclasses should implement this method to parse the response and
        identify individual reasoning steps.
        
        Args:
            response (str): The raw response from which to extract steps.
            
        Returns:
            List[str]: A list of extracted reasoning steps.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def __str__(self) -> str:
        """
        String representation of the reasoner.
        
        Returns:
            str: A string describing the reasoner with its model name.
        """
        return f"{self.__class__.__name__}(model_name={self.model_name})"
