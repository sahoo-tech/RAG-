"""
Base agent class with Ollama integration.
"""

from typing import Dict, Any, Optional
import time
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    
from config import get_settings
from utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


class BaseAgent:
    """Base class for all agents in the system."""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.use_ollama = OLLAMA_AVAILABLE
        
        if not self.use_ollama:
            logger.warning(f"{name}: Ollama not available, using deterministic fallback")
        else:
            logger.info(f"{name} initialized with Ollama", model=settings.ollama_model)
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input and return output.
        To be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement process method")
    
    def _call_ollama(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Call Ollama LLM with a prompt."""
        if not self.use_ollama:
            return self._deterministic_fallback(prompt)
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = ollama.chat(
                model=settings.ollama_model,
                messages=messages,
                options={
                    "temperature": settings.agent_temperature,
                    "num_predict": 500
                }
            )
            
            return response['message']['content']
        
        except Exception as e:
            logger.error(f"{self.name}: Ollama call failed", error=str(e))
            return self._deterministic_fallback(prompt)
    
    def _deterministic_fallback(self, prompt: str) -> str:
        """
        Deterministic fallback when Ollama is not available.
        Returns a simple response based on the prompt.
        """
        logger.info(f"{self.name}: Using deterministic fallback")
        return f"[Deterministic response from {self.name}]"
    
    def _create_response(self, output: Dict[str, Any], processing_time_ms: float) -> Dict[str, Any]:
        """Create standardized agent response."""
        return {
            "agent_name": self.name,
            "output": output,
            "processing_time_ms": processing_time_ms,
            "metadata": {
                "role": self.role,
                "timestamp": time.time()
            }
        }
