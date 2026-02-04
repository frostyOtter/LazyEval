"""Langfuse integration for LazyEval platform."""

from langfuse import Langfuse
from loguru import logger

from src.config.models import LangfuseConfig
from src.evaluation.models import EvalResult


class LangfuseExporter:
    """Export evaluation results and traces to Langfuse for LLM-as-Judge evaluation."""
    
    def __init__(self, config: LangfuseConfig):
        """
        Initialize Langfuse client.
        
        Args:
            config: Langfuse configuration with API keys
        """
        self.config = config
        self.client = Langfuse(
            public_key=config.public_key,
            secret_key=config.secret_key,
            host=config.host
        )
        logger.info(f"Initialized Langfuse client at {config.host}")
    
    def export_results(self, results: list[EvalResult], run_name: str):
        """
        Export evaluation results to Langfuse.
        
        Creates a trace for the evaluation run and generation spans for each result.
        Langfuse will perform LLM-as-Judge evaluation using the expected_response
        as reference.
        
        Args:
            results: List of evaluation results
            run_name: Name for this evaluation run
        """
        logger.info(f"Exporting {len(results)} results to Langfuse as run: {run_name}")
        
        # Create trace for the entire evaluation run
        trace = self.client.trace(
            name=run_name,
            metadata={
                "total_items": len(results),
                "platform": "LazyEval"
            }
        )
        
        # Create a generation span for each evaluation result
        for result in results:
            trace.generation(
                name="agriculture_eval",
                input=f"{result.instruction}\n\n{result.input_text}",
                output=result.model_output,
                metadata={
                    "item_id": result.item_id,
                    "expected_response": result.expected_response,
                    "latency_ms": result.latency_ms,
                    "timestamp": result.timestamp.isoformat()
                }
            )
        
        # Flush to ensure all data is sent to Langfuse
        self.client.flush()
        logger.info(f"Successfully exported results to Langfuse: {run_name}")
