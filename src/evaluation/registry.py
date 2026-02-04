"""
Evaluation registry for mapping datasets to metrics.
"""

from typing import Callable, List, Dict
from src.metrics.answer_relevance import calculate_answer_relevance
from src.metrics.answer_accuracy import calculate_answer_accuracy

# Type alias for metric function
# Metric functions take (prediction, reference) or (query, prediction) etc.
# For simplicity in this registry, we assume a standard interface or handle wrappers within the runner
# But to map names to actual functions:

METRIC_FUNCTIONS = {
    "answer_relevance": calculate_answer_relevance,
    "answer_accuracy": calculate_answer_accuracy,
}

DATASET_METRICS_MAP = {
    "Mahesh2841/Agriculture": ["answer_relevance"],
}

def get_metric_functions(dataset_name: str) -> Dict[str, Callable]:
    """
    Retrieve the dictionary of metric functions configured for a specific dataset.
    
    Args:
        dataset_name: Name of the dataset being evaluated.
        
    Returns:
        Dictionary where key is metric name and value is the callable function.
        Returns a default empty dict or specific default metrics if needed.
    """
    metric_names = DATASET_METRICS_MAP.get(dataset_name, [])
    
    metrics = {}
    for name in metric_names:
        if name in METRIC_FUNCTIONS:
            metrics[name] = METRIC_FUNCTIONS[name]
            
    return metrics
