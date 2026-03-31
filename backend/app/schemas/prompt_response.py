from typing import List

from pydantic import BaseModel


class PromptVariant(BaseModel):
    label: str
    prompt: str


class PromptImproveResponse(BaseModel):
    original_prompt: str
    prompt_type: str
    hidden_goal: str
    missing_pieces: List[str]
    improved_prompt: str
    explanation: str
    confidence_score: float
    expected_output_preview: str
    variants: List[PromptVariant]