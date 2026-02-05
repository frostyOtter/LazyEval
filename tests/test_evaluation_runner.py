"""Tests for evaluation runner."""

from unittest.mock import MagicMock, patch

from src.config.models import EvaluationConfig
from src.datasets.models import AgricultureDatasetItem
from src.evaluation.runner import EvaluationRunner
from src.models.client import ModelClient


@patch("src.evaluation.runner.update_trace")
def test_evaluation_runner(mock_update_trace):
    """Test EvaluationRunner with mocked components."""
    # Create mock dataset items
    mock_items = [
        AgricultureDatasetItem(
            instruction="Answer the question",
            input="What is soil?",
            response="Soil is the upper layer of earth.",
        ),
        AgricultureDatasetItem(
            instruction="Answer the question",
            input="What is erosion?",
            response="Erosion is the wearing away of rock.",
        ),
    ]

    # Mock dataset loader
    mock_loader = MagicMock()
    mock_loader.load.return_value = iter(mock_items)
    mock_loader.get_metrics.return_value = []  # Return empty list of metrics

    # Mock model client
    mock_client = MagicMock(spec=ModelClient)
    mock_client.generate.side_effect = [
        ("Generated response 1", 100.0),
        ("Generated response 2", 150.0),
    ]

    # Create runner
    eval_config = EvaluationConfig(skip_on_error=True)
    runner = EvaluationRunner(mock_loader, mock_client, eval_config)

    # Run evaluation
    results = runner.run()

    # Assertions
    assert len(results) == 2
    assert results[0].input_text == "What is soil?"
    assert results[0].model_output == "Generated response 1"
    assert results[0].latency_ms == 100.0
    assert results[1].input_text == "What is erosion?"
    assert results[1].model_output == "Generated response 2"
    assert results[1].latency_ms == 150.0


@patch("src.evaluation.runner.update_trace")
def test_evaluation_runner_error_handling(mock_update_trace):
    """Test error handling in evaluation runner."""
    mock_items = [
        AgricultureDatasetItem(instruction="Test", input="Q1", response="A1"),
        AgricultureDatasetItem(instruction="Test", input="Q2", response="A2"),
    ]

    mock_loader = MagicMock()
    mock_loader.load.return_value = iter(mock_items)

    # Mock client that fails on first call
    mock_client = MagicMock(spec=ModelClient)
    mock_client.generate.side_effect = [Exception("API Error"), ("Success", 100.0)]

    eval_config = EvaluationConfig(skip_on_error=True)
    runner = EvaluationRunner(mock_loader, mock_client, eval_config)

    # Run - should skip first item and continue
    results = runner.run()

    # Should have 1 successful result (second item)
    assert len(results) == 1
    assert results[0].input_text == "Q2"
