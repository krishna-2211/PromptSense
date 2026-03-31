from typing import Literal, Optional

from pydantic import BaseModel, Field


class PromptImproveRequest(BaseModel):
    original_prompt: str = Field(..., min_length=3)
    audience: Optional[
        Literal["general", "beginner", "executive", "technical", "professional"]
    ] = "general"
    output_style: Optional[
        Literal["concise", "detailed", "professional", "structured"]
    ] = "structured"
    additional_context: Optional[str] = None

    # MCP-backed context inputs
    file_id: Optional[str] = None
    web_url: Optional[str] = None

    # Optional direct context fallback
    file_context: Optional[str] = None