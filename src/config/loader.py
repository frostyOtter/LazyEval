"""Configuration loader for LazyEval platform."""

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from loguru import logger

from src.config.models import (
    AppConfig,
    DatasetConfig,
    EvaluationConfig,
    LangfuseConfig,
    ModelConfig,
    OutputConfig,
)


def load_config(config_path: str = "configs/config.yaml") -> AppConfig:
    """
    Load configuration from environment variables and YAML file.

    Environment variables take precedence over YAML configuration for sensitive data.

    Args:
        config_path: Path to the YAML configuration file

    Returns:
        Validated AppConfig instance

    Raises:
        FileNotFoundError: If config file doesn't exist
        ValidationError: If configuration is invalid
    """
    # Load environment variables from .env file
    load_dotenv()
    logger.info("Loaded environment variables from .env file")

    # Load YAML configuration
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_file) as f:
        yaml_config: dict[str, Any] = yaml.safe_load(f)

    logger.info(f"Loaded configuration from {config_path}")

    # Build ModelConfig (env vars override YAML)
    model_config = ModelConfig(
        temperature=yaml_config.get("model", {}).get("temperature", 0.7),
        top_p=yaml_config.get("model", {}).get("top_p", 1.0),
        max_tokens=yaml_config.get("model", {}).get("max_tokens", 1000),
    )

    # Build DatasetConfig
    dataset_config = DatasetConfig(
        name=yaml_config.get("dataset", {}).get("name", "Mahesh2841/Agriculture"),
        max_samples=yaml_config.get("dataset", {}).get("max_samples"),
    )

    # Build EvaluationConfig
    eval_config = EvaluationConfig(
        skip_on_error=yaml_config.get("evaluation", {}).get("skip_on_error", True),
    )

    # Build OutputConfig
    output_config = OutputConfig(
        results_dir=yaml_config.get("output", {}).get("results_dir", "results"),
        log_dir=yaml_config.get("output", {}).get("log_dir", "logs"),
    )

    # Build LangfuseConfig (from env vars only)
    langfuse_config = LangfuseConfig(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY", ""),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY", ""),
        base_url=os.getenv("LANGFUSE_BASE_URL"),
    )

    # Build AppConfig
    app_config = AppConfig(
        model=model_config,
        dataset=dataset_config,
        evaluation=eval_config,
        output=output_config,
        langfuse=langfuse_config,
    )

    logger.info("Configuration loaded and validated successfully")
    return app_config
