"""Tests for exporters (Langfuse and JSON)."""

import json
import os
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
            timestamp=datetime(2024, 1, 1, 12, 0, 0),
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


@pytest.mark.skipif(
    sys.version_info >= (3, 14),
    reason="Langfuse incompatible with Python 3.14+ (Pydantic v1 issue)",
)
def test_langfuse_exporter():
    """Test Langfuse exporter."""
    # Force reload of the module to ensure patches are applied at import time
    if "src.integrations.langfuse_client" in sys.modules:
        del sys.modules["src.integrations.langfuse_client"]

    # Mock observe to be a passthrough decorator
    def mock_observe_decorator(*args, **kwargs):
        def decorator(func):
            return func

        return decorator

    with (
        patch("langfuse.observe", side_effect=mock_observe_decorator),
        patch("langfuse.get_client") as mock_get_client_func,
    ):

        # Setup mock client
        mock_langfuse_client = MagicMock()
        mock_get_client_func.return_value = mock_langfuse_client

        # Import after patching
        from src.config.models import LangfuseConfig
        from src.integrations.langfuse_client import LangfuseExporter

        # Create exporter
        config = LangfuseConfig(
            public_key="pk-test",
            secret_key="sk-test",
            base_url="https://test.langfuse.com",
        )

        with patch.dict(os.environ, {}, clear=True):
            exporter = LangfuseExporter(config)

            # Verify env vars are set
            assert os.environ["LANGFUSE_PUBLIC_KEY"] == "pk-test"
            assert os.environ["LANGFUSE_SECRET_KEY"] == "sk-test"
            assert os.environ["LANGFUSE_HOST"] == "https://test.langfuse.com"

            # Create test results
            results = [
                EvalResult(
                    item_id="1",
                    instruction="Test instruction",
                    input_text="Test input",
                    model_output="Test output",
                    expected_response="Test expected",
                    latency_ms=100.0,
                )
            ]

            # Export
            exporter.export_results(results, "test_run")

            # Verify Langfuse calls
            # Check update_current_trace
            mock_langfuse_client.update_current_trace.assert_called_with(
                name="test_run",
                input=None,
                output=None,
                metadata={"total_items": 1, "platform": "LazyEval"},
            )

            # Check update_current_span
            mock_langfuse_client.update_current_span.assert_called_with(
                name="1",
                input="Test instruction\n\nTest input",
                output="Test output",
                metadata={
                    "item_id": "1",
                    "expected_response": "Test expected",
                    "latency_ms": 100.0,
                    "timestamp": results[0].timestamp.isoformat(),
                },
            )

            # Check flush
            mock_langfuse_client.flush.assert_called_once()
