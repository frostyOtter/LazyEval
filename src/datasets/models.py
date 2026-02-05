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


class MirageDatasetItem(BaseModel):
    """Schema for nlpai-lab/mirage dataset items."""

    query: str = Field(..., description="The question/instruction")
    answer: list[str] = Field(..., description="List of valid answers")
    doc_pool: dict = Field(..., description="Pool of documents/chunks")
    oracle: dict = Field(..., description="Ground truth document info")

    # Generated fields
    item_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this item",
    )

    def format_prompt(self) -> str:
        """
        Format the query and doc_pool into a prompt.

        Returns:
            Formatted prompt string
        """
        # Construct context from doc_pool chunks
        # doc_pool['doc_chunk'] is a list of strings
        chunks = self.doc_pool.get("doc_chunk", [])
        context = "\n\n".join(chunks)

        return f"Context:\n{context}\n\nQuestion:\n{self.query}"

    @property
    def instruction(self) -> str:
        """Alias for query to satisfy EvaluationRunner interface."""
        return self.query

    @property
    def input(self) -> str:
        """Alias for context (doc_pool) to satisfy EvaluationRunner interface."""
        chunks = self.doc_pool.get("doc_chunk", [])
        return "\n\n".join(chunks)

    @property
    def response(self) -> str:
        """Alias for answer to satisfy EvaluationRunner interface."""
        return str(self.answer)
