"""Tests for configuration loading."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from src.config.loader import load_config
from src.config.models import AppConfig


def test_load_config_with_env_vars(tmp_path):
    """Test loading configuration with environment variables."""
    # Create a temporary config file
    config_file = tmp_path / "config.yaml"
    config_file.write_text("""
model:
  temperature: 0.7
  top_p: 1.0
  max_tokens: 1000

dataset:
  name: "Mahesh2841/Agriculture"
  max_samples: 10

evaluation:
  skip_on_error: true

output:
  results_dir: "results"
  log_dir: "logs"
""")
    
    # Set environment variables
    env_vars = {
        "MODEL_NAME": "test-model",
        "MODEL_BASE_URL": "http://test-api.com/v1",
        "MODEL_API_KEY": "test-key",
        "LANGFUSE_PUBLIC_KEY": "pk-test",
        "LANGFUSE_SECRET_KEY": "sk-test",
        "LANGFUSE_HOST": "https://test.langfuse.com"
    }
    
    with patch.dict(os.environ, env_vars, clear=False):
        config = load_config(str(config_file))
    
    # Assertions
    assert isinstance(config, AppConfig)
    assert config.model.model_name == "test-model"
    assert config.model.base_url == "http://test-api.com/v1"
    assert config.model.api_key == "test-key"
    assert config.model.temperature == 0.7
    assert config.dataset.name == "Mahesh2841/Agriculture"
    assert config.dataset.max_samples == 10
    assert config.evaluation.skip_on_error is True
    assert config.langfuse.public_key == "pk-test"


def test_load_config_missing_file():
    """Test error handling when config file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        load_config("nonexistent.yaml")
