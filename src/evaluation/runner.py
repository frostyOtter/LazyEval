"""Sequential evaluation runner for LazyEval platform."""

import inspect

from langfuse import observe
from loguru import logger
from tqdm import tqdm

from src.config.models import EvaluationConfig
from src.datasets.base import BaseDatasetLoader
from src.evaluation.models import EvalResult
from src.integrations.langfuse_client import update_trace
from src.models.client import ModelClient


class EvaluationRunner:
    """Orchestrates sequential evaluation of dataset items through the model."""

    def __init__(
        self,
        dataset_loader: BaseDatasetLoader,
        model_client: ModelClient,
        eval_config: EvaluationConfig,
    ):
        """
        Initialize the evaluation runner.

        Args:
            dataset_loader: Dataset loader instance
            model_client: Model client instance
            eval_config: Evaluation configuration
        """
        self.dataset_loader = dataset_loader
        self.model_client = model_client
        self.eval_config = eval_config

    def run(self) -> list[EvalResult]:
        """
        Run evaluation on all dataset items sequentially.

        Returns:
            List of evaluation results
        """
        results: list[EvalResult] = []

        logger.info("Starting evaluation run")

        # Process items sequentially with progress bar
        for item in tqdm(self.dataset_loader.load(), desc="Evaluating"):
            result = self._process_item(item)
            if result:
                results.append(result)

        logger.info(f"Evaluation complete: {len(results)} items processed successfully")
        return results

    @observe(as_type="trace")
    def _process_item(self, item) -> EvalResult | None:
        """
        Process a single dataset item: generate, evaluate, and return result.

        Args:
            item: Dataset item to process

        Returns:
            EvalResult if successful, None if skipped on error
        """
        try:
            # Format prompt from instruction and input
            prompt = item.format_prompt()

            # Call model API
            logger.debug(f"Processing item {item.item_id}")
            output, latency = self.model_client.generate(prompt)
            update_trace(
                **{
                    "name": item.item_id,
                    "input": prompt,
                    "output": output,
                    "metadata": {
                        "latency_ms": latency,
                    },
                }
            )

            # Create evaluation result
            # Get metrics directly from the dataset loader
            metric_funcs = self.dataset_loader.get_metrics()

            # Prepare context for metrics
            eval_context = {
                "prediction": output,
                "reference": item.response,
                "instruction": item.instruction,
                "query": item.instruction,
                "input": item.input,
            }

            computed_metrics = {}
            for func in metric_funcs:
                try:
                    # Call the metric function
                    score = func(**eval_context)
                    computed_metrics[func.__name__] = score

                except Exception as metric_err:
                    logger.error(
                        f"Error calculating metric {func.__name__}: {metric_err}"
                    )

            result = EvalResult(
                item_id=item.item_id,
                instruction=item.instruction,
                input_text=item.input,
                model_output=output,
                expected_response=item.response,
                latency_ms=latency,
                metrics=computed_metrics,
            )

            logger.debug(f"Completed item {item.item_id}")
            return result

        except Exception as e:
            if self.eval_config.skip_on_error:
                logger.error(f"Error processing item {item.item_id}: {e}")
                return None
            else:
                logger.error(f"Fatal error processing item {item.item_id}: {e}")
                raise
