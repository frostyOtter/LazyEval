"""JSON export for evaluation results."""

import json
from datetime import datetime
from pathlib import Path

from loguru import logger

from src.evaluation.models import EvalResult


class JSONExporter:
    """Export evaluation results to timestamped JSON files for backup."""
    
    def __init__(self, output_dir: str):
        """
        Initialize JSON exporter.
        
        Args:
            output_dir: Directory to save JSON files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        logger.info(f"Initialized JSON exporter with output directory: {self.output_dir}")
    
    def export_results(self, results: list[EvalResult]) -> Path:
        """
        Export evaluation results to a timestamped JSON file.
        
        Args:
            results: List of evaluation results
            
        Returns:
            Path to the created JSON file
        """
        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"results_{timestamp}.json"
        
        # Convert results to JSON-serializable dicts
        results_dict = [r.model_dump(mode='json') for r in results]
        
        # Write to file with pretty formatting
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to {filename} ({len(results)} items)")
        return filename
