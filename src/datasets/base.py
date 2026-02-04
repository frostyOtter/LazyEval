"""Base interface for dataset loaders."""

from abc import ABC, abstractmethod
from typing import Iterator

from pydantic import BaseModel


class BaseDatasetLoader(ABC):
    """Abstract base class for dataset loaders."""
    
    @abstractmethod
    def load(self) -> Iterator[BaseModel]:
        """
        Load and yield dataset items.
        
        Yields:
            Dataset items as Pydantic models
        """
        pass
    
    @abstractmethod
    def validate_item(self, item: dict) -> BaseModel | None:
        """
        Validate and parse a single dataset item.
        
        Args:
            item: Raw item dictionary from dataset
            
        Returns:
            Validated Pydantic model or None if invalid
        """
        pass
