from pydantic import BaseModel


class ClassifyIntentOutput(BaseModel):
    prompt_type: str
    hidden_goal: str


class DetectMissingPiecesOutput(BaseModel):
    missing_pieces: list[str]


class StructureInstructionOutput(BaseModel):
    structured_prompt: str


class OptimizePromptOutput(BaseModel):
    improved_prompt: str