"""Mirage dataset loader from HuggingFace."""

from pathlib import Path
from typing import Iterator

from loguru import logger
from pydantic import ValidationError

from datasets import load_dataset
from src.config.models import DatasetConfig, EvaluationConfig
from src.datasets.base import BaseDatasetLoader
from src.datasets.models import MirageDatasetItem
from src.metrics.answer_correctness import calculate_answer_correctness


class MirageDatasetLoader(BaseDatasetLoader):
    """Loader for the nlpai-lab/mirage dataset from HuggingFace."""

    def __init__(self, dataset_config: DatasetConfig, eval_config: EvaluationConfig):
        """
        Initialize the Mirage dataset loader.

        Args:
            dataset_config: Dataset configuration
            eval_config: Evaluation configuration (for error handling)
        """
        self.dataset_config = dataset_config
        self.eval_config = eval_config

    def get_metrics(self) -> list[callable]:
        """
        Get the list of metric functions.
        """
        return [calculate_answer_correctness]

    def load(self) -> Iterator[MirageDatasetItem]:
        """
        Load the Mirage dataset from HuggingFace.

        Yields:
            Validated MirageDatasetItem instances
        """
        logger.info(f"Loading dataset: {self.dataset_config.name}")

        try:
            # Determine cache directory
            project_root = Path(__file__).resolve().parent.parent.parent
            dataset_cache_dir = project_root / "data"

            logger.info(f"Using dataset cache directory: {dataset_cache_dir}")

            # Load dataset
            dataset = load_dataset(
                self.dataset_config.name,
                split="train",
                cache_dir=str(dataset_cache_dir),
            )
            logger.info(f"Loaded {len(dataset)} items from HuggingFace")

            # Apply max_samples limit if specified
            if self.dataset_config.max_samples is not None:
                original_count = len(dataset)
                dataset = dataset.select(
                    range(min(self.dataset_config.max_samples, original_count))
                )
                logger.info(
                    f"Limited to {len(dataset)} samples (from {original_count})"
                )

            # Iterate and validate items
            successful_count = 0
            failed_count = 0

            for idx, item in enumerate(dataset):
                validated = self.validate_item(item)
                if validated:
                    successful_count += 1
                    yield validated
                else:
                    failed_count += 1

            logger.info(
                f"Dataset loading complete: {successful_count} items loaded, "
                f"{failed_count} items skipped due to validation errors"
            )

        except Exception as e:
            logger.error(f"Failed to load dataset {self.dataset_config.name}: {e}")
            if not self.eval_config.skip_on_error:
                raise

    def validate_item(self, item: dict) -> MirageDatasetItem | None:
        """
        Validate and parse a single dataset item.
        """
        try:
            return MirageDatasetItem(**item)
        except ValidationError as e:
            if self.eval_config.skip_on_error:
                logger.warning(f"Skipping invalid item: {e}")
                return None
            else:
                raise
