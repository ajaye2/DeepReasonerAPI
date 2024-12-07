from reasonedge.base import BaseReasoner
from reasoners.lm import OpenAIModel
from typing import Any, Dict, List, Optional, Union
import time
import re

class ChainOfThoughtReasoner(BaseReasoner):
    """
    A reasoner that applies the Chain of Thought (CoT) methodology to generate
    structured reasoning responses using a language model.
    """

    def __init__(self, model_name: str, temperature: float = 1.0, use_azure: bool = True, **kwargs):
        """
        Initialize the ChainOfThoughtReasoner with a specified model and parameters.

        Args:
            model_name (str): The name of the language model to be used.
            use_azure (bool): Flag to determine if Azure should be used. Defaults to True.
            **kwargs: Additional keyword arguments for specific implementations.
        """
        super().__init__(model_name, temperature, **kwargs)
        self.model = OpenAIModel(model=model_name, use_azure=use_azure)
        
    def reason(self, 
               prompt: str, 
               context: Optional[Union[str, List[str]]] = None,
               temperature: Optional[float] = 1.0,
               **kwargs) -> Dict[str, Any]:
        """
        Apply chain of thought reasoning to the given prompt.

        This method processes the input prompt and context to generate a reasoned response
        using a step-by-step approach.

        Args:
            prompt (str): The input prompt to reason about.
            context (Optional[Union[str, List[str]]]): Additional context for reasoning.
            temperature (float, optional): Sampling temperature. Defaults to 1.0.
            **kwargs: Additional keyword arguments for specific implementations.
            
        Returns:
            Dict[str, Any]: A dictionary containing the response, reasoning steps, and metadata.
        """
        start_time = time.time()
        
        # Define the system prompt to guide the reasoning process
        system_prompt = """
                        Let's think step by step.
                        Each step should be a list item, with "Step X:" as the prefix, e.g. "Step 1: ..."
                        After each reasoning step, output a newline character.
                        When you have finished your reasoning, provide your final answer as a list item, with "Answer:" as the prefix, e.g. "Answer: ..."
                        Always think before you answer.
                        """
        
        # Generate response from the model
        raw_response = self.model.generate(
            [prompt],
            temperature=temperature,
            system_prompt=system_prompt
        ).text[0]
        
        # Extract reasoning steps and determine the final response
        steps = self._extract_reasoning_steps(raw_response)
        final_response = steps[-1] if steps else raw_response
        
        # Format and return the response
        return self.format_response(
            response=raw_response,
            reasoning_steps=steps,
            final_answer=final_response,
            start_time=start_time,
            temperature=temperature
        )

    def _extract_reasoning_steps(self, raw_response: str) -> List[str]:
        """
        Extract individual reasoning steps from the raw response.

        This method parses the raw response to identify and extract each reasoning step
        and the final answer.

        Args:
            raw_response (str): The raw response from the model.
            
        Returns:
            List[str]: A list of reasoning steps extracted from the response.
        """
        # Split the response by newlines and filter out empty lines
        lines = [line.strip() for line in raw_response.split('\n') if line.strip()]
        
        steps = []
        for line in lines:
            # Remove leading "- " or "* " bullet if present
            normalized_line = re.sub(r"^[\-\*\•]\s*", "", line)
            
            # Check if the normalized line is a step or an answer line
            # Match formats like "Step 1:", "Step 2:", ignoring case, and allowing some spacing
            if re.match(r"(?i)^step\s*\d+\:", normalized_line):
                steps.append(normalized_line)
            elif re.match(r"(?i)^answer:", normalized_line):
                steps.append(normalized_line)
            # If we haven't found any steps yet, still capture the line as a starting point
            elif not steps and normalized_line:
                steps.append(normalized_line)
        
        return steps
