"""OpenAI-compatible model client for LazyEval platform."""

import time
from typing import Tuple

from loguru import logger
from openai import OpenAI
from openai.types.chat import ChatCompletion

from src.config.models import ModelConfig


class ModelClient:
    """Client for interacting with OpenAI-compatible API endpoints (vLLM, etc.)."""
    
    def __init__(self, config: ModelConfig):
        """
        Initialize the model client.
        
        Args:
            config: Model configuration including endpoint and API key
        """
        self.config = config
        self.client = OpenAI(
            base_url=config.base_url,
            api_key=config.api_key
        )
        logger.info(f"Initialized model client for {config.model_name} at {config.base_url}")
    
    def generate(self, prompt: str) -> Tuple[str, float]:
        """
        Generate text completion from the model.
        
        Args:
            prompt: Input prompt for the model
            
        Returns:
            Tuple of (model_output, latency_ms)
            
        Raises:
            Exception: If API call fails after retries
        """
        start_time = time.time()
        
        try:
            response: ChatCompletion = self.client.chat.completions.create(
                model=self.config.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                max_tokens=self.config.max_tokens,
                stream=False
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            # Extract the response text
            output = response.choices[0].message.content or ""
            
            logger.debug(f"Generated response in {latency_ms:.2f}ms")
            return output, latency_ms
            
        except Exception as e:
            logger.error(f"Model API error: {e}")
            raise
