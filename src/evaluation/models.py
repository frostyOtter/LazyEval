"""Evaluation result models."""

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class EvalResult(BaseModel):
    """Result of evaluating a single dataset item with the model."""
    
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    item_id: str = Field(..., description="Unique identifier for the dataset item")
    instruction: str = Field(..., description="Instruction given to the model")
    input_text: str = Field(..., description="Input text/question")
    model_output: str = Field(..., description="Generated response from the model")
    expected_response: str = Field(..., description="Expected/reference response (ground truth)")
    latency_ms: float = Field(..., description="Time taken for model inference in milliseconds")
    metrics: dict[str, float] = Field(default_factory=dict, description="Computed evaluation metrics")
    evaluation_details: dict = Field(default_factory=dict, description="Detailed evaluation results/logs")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC), description="When this evaluation was performed")
