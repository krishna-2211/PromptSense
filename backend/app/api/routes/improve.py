from fastapi import APIRouter, HTTPException
import traceback

from app.schemas.prompt_request import PromptImproveRequest
from app.schemas.prompt_response import PromptImproveResponse
from app.services.prompt_orchestrator import PromptOrchestrator

router = APIRouter(tags=["Prompt Improvement"])

orchestrator = PromptOrchestrator()


@router.post("/improve", response_model=PromptImproveResponse)
def improve_prompt(payload: PromptImproveRequest) -> PromptImproveResponse:
    try:
        return orchestrator.improve_prompt(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(exc)}") from exc