from src.evaluation.registry import get_metric_functions, METRIC_FUNCTIONS, DATASET_METRICS_MAP

def test_get_metric_functions_found():
    """Test retrieving metrics for a known dataset."""
    # Ensure there's a known dataset
    dataset_name = "Mahesh2841/Agriculture"
    expected_metrics = ["answer_relevance"]
    
    metrics = get_metric_functions(dataset_name)
    
    assert len(metrics) == 1
    assert "answer_relevance" in metrics
    assert callable(metrics["answer_relevance"])

def test_get_metric_functions_not_found():
    """Test retrieving metrics for an unknown dataset."""
    metrics = get_metric_functions("Unknown/Dataset")
    assert metrics == {}

def test_registry_integration():
    """Ensure mapped function names exist in METRIC_FUNCTIONS."""
    for dataset, metric_names in DATASET_METRICS_MAP.items():
        for name in metric_names:
            assert name in METRIC_FUNCTIONS, f"Metric '{name}' for dataset '{dataset}' not implemented"
