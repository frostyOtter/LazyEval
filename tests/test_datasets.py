"""Tests for dataset loading."""

from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from src.config.models import DatasetConfig, EvaluationConfig
from src.datasets.agriculture import AgricultureDatasetLoader
from src.datasets.models import AgricultureDatasetItem


def test_agriculture_dataset_item_validation():
    """Test AgricultureDatasetItem validation."""
    # Valid item
    item = AgricultureDatasetItem(
        instruction="Answer the question", input="What is 2+2?", response="4"
    )

    assert item.instruction == "Answer the question"
    assert item.input == "What is 2+2?"
    assert item.response == "4"
    assert item.item_id is not None  # Auto-generated UUID

    # Test format_prompt
    prompt = item.format_prompt()
    assert prompt == "Answer the question\n\nWhat is 2+2?"


def test_agriculture_dataset_item_invalid():
    """Test validation errors for invalid items."""
    with pytest.raises(ValidationError):
        AgricultureDatasetItem(
            instruction="Test",
            # Missing required fields
        )


@patch("src.datasets.agriculture.load_dataset")
def test_agriculture_dataset_loader(mock_load_dataset):
    """Test AgricultureDatasetLoader with mocked HuggingFace dataset."""
    # Mock dataset
    mock_dataset = [
        {
            "instruction": "Answer the question",
            "input": "What is soil?",
            "response": "Soil is the upper layer of earth.",
        },
        {
            "instruction": "Answer the question",
            "input": "What is erosion?",
            "response": "Erosion is the wearing away of rock or soil.",
        },
    ]

    mock_hf_dataset = MagicMock()
    mock_hf_dataset.__len__ = MagicMock(return_value=len(mock_dataset))
    mock_hf_dataset.__iter__ = MagicMock(return_value=iter(mock_dataset))
    mock_load_dataset.return_value = mock_hf_dataset

    # Create loader
    dataset_config = DatasetConfig(name="Mahesh2841/Agriculture", max_samples=None)
    eval_config = EvaluationConfig(skip_on_error=True)
    loader = AgricultureDatasetLoader(dataset_config, eval_config)

    # Load items
    items = list(loader.load())

    # Assertions
    assert len(items) == 2
    assert all(isinstance(item, AgricultureDatasetItem) for item in items)
    assert items[0].input == "What is soil?"
    assert items[1].input == "What is erosion?"


@patch("src.datasets.agriculture.load_dataset")
def test_agriculture_dataset_loader_with_max_samples(mock_load_dataset):
    """Test that max_samples limits the number of items."""
    mock_dataset = [
        {"instruction": "Test", "input": f"Q{i}", "response": f"A{i}"}
        for i in range(100)
    ]

    mock_hf_dataset = MagicMock()
    mock_hf_dataset.__len__ = MagicMock(return_value=100)

    # Create selected subset
    selected_subset = MagicMock()
    selected_subset.__iter__ = MagicMock(return_value=iter(mock_dataset[:10]))
    selected_subset.__len__ = MagicMock(return_value=10)

    mock_hf_dataset.select = MagicMock(return_value=selected_subset)
    mock_load_dataset.return_value = mock_hf_dataset

    dataset_config = DatasetConfig(name="Mahesh2841/Agriculture", max_samples=10)
    eval_config = EvaluationConfig(skip_on_error=True)
    loader = AgricultureDatasetLoader(dataset_config, eval_config)

    items = list(loader.load())

    # Should call select with the right range
    mock_hf_dataset.select.assert_called_once()
