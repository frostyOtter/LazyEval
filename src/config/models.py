"""Configuration models for LazyEval platform."""

from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    """Configuration for the language model API."""

    temperature: float = Field(
        default=0.7, ge=0.0, le=2.0, description="Sampling temperature"
    )
    top_p: float = Field(
        default=1.0, ge=0.0, le=1.0, description="Nucleus sampling parameter"
    )
    max_tokens: int = Field(
        default=1000, gt=0, description="Maximum tokens to generate"
    )


class DatasetConfig(BaseModel):
    """Configuration for dataset loading."""

    name: str = Field(
        default="Mahesh2841/Agriculture", description="HuggingFace dataset name"
    )
    max_samples: int | None = Field(
        default=None, description="Maximum number of samples to process (None = all)"
    )


class EvaluationConfig(BaseModel):
    """Configuration for evaluation execution."""

    skip_on_error: bool = Field(
        default=True, description="Skip and log errors instead of failing"
    )


class OutputConfig(BaseModel):
    """Configuration for output directories."""

    results_dir: str = Field(
        default="results", description="Directory for JSON result backups"
    )
    log_dir: str = Field(default="logs", description="Directory for log files")


class LangfuseConfig(BaseModel):
    """Configuration for Langfuse integration."""

    public_key: str = Field(..., description="Langfuse public API key")
    secret_key: str = Field(..., description="Langfuse secret API key")
    base_url: str = Field(
        default="https://cloud.langfuse.com", description="Langfuse base URL"
    )


class AppConfig(BaseModel):
    """Root configuration model for the application."""

    model: ModelConfig
    dataset: DatasetConfig
    evaluation: EvaluationConfig
    output: OutputConfig
    langfuse: LangfuseConfig
