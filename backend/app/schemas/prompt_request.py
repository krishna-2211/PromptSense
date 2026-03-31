from typing import Literal, Optional

from pydantic import BaseModel, Field


class PromptImproveRequest(BaseModel):
    original_prompt: str = Field(..., min_length=3, description="User's raw prompt")
    audience: Optional[
        Literal["general", "beginner", "executive", "technical", "professional"]
        ] = "general"
    output_style: Optional[Literal["concise", "detailed", "professional", "structured"]] = "structured"
    additional_context: Optional[str] = Field(
        default=None,
        description="Optional extra user-provided context",
    )
    file_context: Optional[str] = Field(
        default=None,
        description="Optional extracted content from uploaded file",
    )