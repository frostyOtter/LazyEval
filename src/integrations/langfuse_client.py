import os
from typing import Any

from langfuse import get_client, observe
from loguru import logger

from src.config.models import LangfuseConfig
from src.evaluation.models import EvalResult

# Initialize global Langfuse client
langfuse_client = get_client()


def _generate_payload(observation: dict) -> dict:
    """Generate payload for Langfuse observation update."""
    return {
        "name": observation.get("name"),
        "input": observation.get("input"),
        "output": observation.get("output"),
        "metadata": observation.get("metadata"),
    }


def update_observation(**kwargs: Any) -> None:
    """Update current observation."""
    payload = _generate_payload(kwargs)
    langfuse_client.update_current_observation(**payload)


def update_trace(**kwargs: Any) -> None:
    """Update current trace."""
    payload = _generate_payload(kwargs)
    langfuse_client.update_current_trace(**payload)


def update_span(**kwargs: Any) -> None:
    """Update current span."""
    payload = _generate_payload(kwargs)
    langfuse_client.update_current_span(**payload)


class LangfuseExporter:
    """Export evaluation results and traces to Langfuse for LLM-as-Judge evaluation."""

    def __init__(self, config: LangfuseConfig):
        """
        Initialize Langfuse integration.

        Sets environment variables for the global Langfuse client to use.

        Args:
            config: Langfuse configuration with API keys
        """
        self.config = config

        # Set environment variables for the singleton client
        os.environ["LANGFUSE_PUBLIC_KEY"] = config.public_key
        os.environ["LANGFUSE_SECRET_KEY"] = config.secret_key
        os.environ["LANGFUSE_HOST"] = config.base_url

        logger.info(f"Configured Langfuse environment for {config.base_url}")

    def export_results(self, results: list[EvalResult], run_name: str):
        """
        Export evaluation results to Langfuse.

        Creates a trace for the evaluation run and generation spans for each result.

        Args:
            results: List of evaluation results
            run_name: Name for this evaluation run
        """
        logger.info(f"Exporting {len(results)} results to Langfuse as run: {run_name}")

        # Process each result
        for result in results:
            self._export_single_result(result)

        # Ensure all data is sent
        langfuse_client.flush()
        logger.info(f"Successfully exported results to Langfuse: {run_name}")

    @observe(as_type="span")
    def _export_single_result(self, result: EvalResult):
        """
        Export a single evaluation result as a span.

        Args:
            result: The evaluation result to export
        """
        # Update span details
        update_span(
            name=result.item_id,
            input=f"{result.instruction}\n\n{result.input_text}",
            output=result.model_output,
            metadata={
                "item_id": result.item_id,
                "expected_response": result.expected_response,
                "latency_ms": result.latency_ms,
                "timestamp": result.timestamp.isoformat(),
            },
        )
