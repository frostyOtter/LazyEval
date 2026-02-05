"""Dataset models for LazyEval platform."""

import uuid

from pydantic import BaseModel, Field


class AgricultureDatasetItem(BaseModel):
    """Schema for Mahesh2841/Agriculture dataset items."""

    instruction: str = Field(..., description="Instruction for the task")
    input: str = Field(..., description="Input text/question for the model")
    response: str = Field(..., description="Expected/reference response (ground truth)")

    # Generated fields
    item_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this item",
    )

    def format_prompt(self) -> str:
        """
        Format the instruction and input into a prompt for the model.

        Returns:
            Formatted prompt string
        """
        return f"{self.instruction}\n\n{self.input}"
