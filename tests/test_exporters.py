"""Tests for exporters (Langfuse and JSON)."""

import json
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.evaluation.models import EvalResult
from src.integrations.json_export import JSONExporter


def test_json_exporter(tmp_path):
    """Test JSON exporter."""
    # Create exporter with temp directory
    exporter = JSONExporter(str(tmp_path))
    
    # Create test results
    results = [
        EvalResult(
            item_id="1",
            instruction="Test instruction",
            input_text="Test input",
            model_output="Test output",
            expected_response="Test expected",
            latency_ms=100.0,
            timestamp=datetime(2024, 1, 1, 12, 0, 0)
        )
    ]
    
    # Export
    json_file = exporter.export_results(results)
    
    # Verify file was created
    assert json_file.exists()
    assert json_file.name.startswith("results_")
    assert json_file.suffix == ".json"
    
    # Verify content
    with open(json_file) as f:
        data = json.load(f)
    
    assert len(data) == 1
    assert data[0]["item_id"] == "1"
    assert data[0]["input_text"] == "Test input"
    assert data[0]["model_output"] == "Test output"


@pytest.mark.skipif(sys.version_info >= (3, 14), reason="Langfuse incompatible with Python 3.14+ (Pydantic v1 issue)")
@patch('src.integrations.langfuse_client.Langfuse')
def test_langfuse_exporter(mock_langfuse_class):
    """Test Langfuse exporter."""
    from src.config.models import LangfuseConfig
    from src.integrations.langfuse_client import LangfuseExporter
    
    # Mock Langfuse client
    mock_client = MagicMock()
    mock_trace = MagicMock()
    mock_client.trace.return_value = mock_trace
    mock_langfuse_class.return_value = mock_client
    
    # Create exporter
    config = LangfuseConfig(
        public_key="pk-test",
        secret_key="sk-test",
        host="https://test.langfuse.com"
    )
    exporter = LangfuseExporter(config)
    
    # Create test results
    results = [
        EvalResult(
            item_id="1",
            instruction="Test instruction",
            input_text="Test input",
            model_output="Test output",
            expected_response="Test expected",
            latency_ms=100.0
        )
    ]
    
    # Export
    exporter.export_results(results, "test_run")
    
    # Verify Langfuse calls
    mock_client.trace.assert_called_once()
    mock_trace.generation.assert_called_once()
    mock_client.flush.assert_called_once()
    
    # Verify generation call
    gen_call = mock_trace.generation.call_args[1]
    assert gen_call['input'] == "Test instruction\n\nTest input"
    assert gen_call['output'] == "Test output"
    assert gen_call['metadata']['expected_response'] == "Test expected"
