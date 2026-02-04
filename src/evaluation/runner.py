"""Sequential evaluation runner for LazyEval platform."""

from loguru import logger
from tqdm import tqdm

from src.config.models import EvaluationConfig
from src.datasets.base import BaseDatasetLoader
from src.evaluation.models import EvalResult
from src.models.client import ModelClient
from src.evaluation.registry import get_metric_functions


class EvaluationRunner:
    """Orchestrates sequential evaluation of dataset items through the model."""
    
    def __init__(
        self,
        dataset_loader: BaseDatasetLoader,
        model_client: ModelClient,
        eval_config: EvaluationConfig
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
            try:
                # Format prompt from instruction and input
                prompt = item.format_prompt()
                
                # Call model API
                logger.debug(f"Processing item {item.item_id}")
                output, latency = self.model_client.generate(prompt)
                
                # Create evaluation result
                # Calculate metrics
                # TODO: Pass dataset name from config or loader
                dataset_name = self.eval_config.dataset_name if hasattr(self.eval_config, "dataset_name") else "Mahesh2841/Agriculture" 
                metric_funcs = get_metric_functions(dataset_name)
                
                computed_metrics = {}
                for name, func in metric_funcs.items():
                    try:
                        # Logic to dispatch arguments based on metric signature
                        # Minimal implementation specific to current supported metrics
                        if name == "answer_relevance":
                            score = func(query=item.instruction, prediction=output)
                        elif name == "answer_accuracy":
                            score = func(prediction=output, reference=item.response)
                        else:
                            score = 0.0 # Placeholder
                        
                        computed_metrics[name] = score
                    except Exception as metric_err:
                        logger.error(f"Error calculating metric {name}: {metric_err}")

                result = EvalResult(
                    item_id=item.item_id,
                    instruction=item.instruction,
                    input_text=item.input,
                    model_output=output,
                    expected_response=item.response,
                    latency_ms=latency,
                    metrics=computed_metrics
                )
                
                results.append(result)
                logger.debug(f"Completed item {item.item_id}")
                
            except Exception as e:
                if self.eval_config.skip_on_error:
                    logger.error(f"Error processing item {item.item_id}: {e}")
                    continue
                else:
                    logger.error(f"Fatal error processing item {item.item_id}: {e}")
                    raise
        
        logger.info(f"Evaluation complete: {len(results)} items processed successfully")
        return results
