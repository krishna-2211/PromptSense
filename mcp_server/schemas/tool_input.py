from typing import Literal, Optional

from pydantic import BaseModel, Field


class ClassifyIntentInput(BaseModel):
    prompt: str = Field(..., min_length=1)


class DetectMissingPiecesInput(BaseModel):
    prompt: str = Field(..., min_length=1)
    prompt_type: str
    audience: Optional[str] = "general"
    output_style: Optional[str] = "structured"
    additional_context: Optional[str] = None
    file_context: Optional[str] = None


class StructureInstructionInput(BaseModel):
    original_prompt: str = Field(..., min_length=1)
    prompt_type: str
    hidden_goal: str
    missing_pieces: list[str]
    audience: Optional[str] = "general"
    output_style: Optional[str] = "structured"
    additional_context: Optional[str] = None
    file_context: Optional[str] = None


class OptimizePromptInput(BaseModel):
    structured_prompt: str = Field(..., min_length=1)
    prompt_type: str