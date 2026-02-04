"""Agriculture dataset loader from HuggingFace."""

from typing import Iterator

from loguru import logger
from pydantic import ValidationError

from datasets import load_dataset
from src.config.models import DatasetConfig, EvaluationConfig
from src.datasets.base import BaseDatasetLoader
from src.datasets.models import AgricultureDatasetItem


class AgricultureDatasetLoader(BaseDatasetLoader):
    """Loader for the Mahesh2841/Agriculture dataset from HuggingFace."""
    
    def __init__(self, dataset_config: DatasetConfig, eval_config: EvaluationConfig):
        """
        Initialize the Agriculture dataset loader.
        
        Args:
            dataset_config: Dataset configuration
            eval_config: Evaluation configuration (for error handling)
        """
        self.dataset_config = dataset_config
        self.eval_config = eval_config
    
    def load(self) -> Iterator[AgricultureDatasetItem]:
        """
        Load the Agriculture dataset from HuggingFace.
        
        Yields:
            Validated AgricultureDatasetItem instances
        """
        logger.info(f"Loading dataset: {self.dataset_config.name}")
        
        try:
            # Load dataset from HuggingFace
            dataset = load_dataset(self.dataset_config.name, split="train")
            logger.info(f"Loaded {len(dataset)} items from HuggingFace")
            
            # Apply max_samples limit if specified
            if self.dataset_config.max_samples is not None:
                original_count = len(dataset)
                dataset = dataset.select(range(min(self.dataset_config.max_samples, original_count)))
                logger.info(f"Limited to {len(dataset)} samples (from {original_count})")
            
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
    
    def validate_item(self, item: dict) -> AgricultureDatasetItem | None:
        """
        Validate and parse a single dataset item.
        
        Args:
            item: Raw item dictionary from HuggingFace dataset
            
        Returns:
            Validated AgricultureDatasetItem or None if validation fails
        """
        try:
            return AgricultureDatasetItem(**item)
        except ValidationError as e:
            if self.eval_config.skip_on_error:
                logger.warning(f"Skipping invalid item: {e}")
                return None
            else:
                raise
