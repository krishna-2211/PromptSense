from app.schemas.prompt_request import PromptImproveRequest
from app.schemas.prompt_response import PromptImproveResponse, PromptVariant
from app.services.prompt_improver import PromptImprover
from app.services.explanation_service import ExplanationService
from app.services.variant_generator import VariantGenerator
from app.prompt_engine.classifier import classify_prompt_type
from app.prompt_engine.context_detector import detect_missing_pieces, extract_hidden_goal
from app.services.output_preview_service import OutputPreviewService


class PromptOrchestrator:
    def __init__(self) -> None:
        self.improver = PromptImprover()
        self.explainer = ExplanationService()
        self.variant_generator = VariantGenerator()
        self.preview_service = OutputPreviewService()

    def improve_prompt(self, payload: PromptImproveRequest) -> PromptImproveResponse:
        prompt = payload.original_prompt.strip()
        if not prompt:
            raise ValueError("Prompt cannot be empty.")

        prompt_type = classify_prompt_type(prompt)
        hidden_goal = extract_hidden_goal(prompt, prompt_type)

        missing_pieces = detect_missing_pieces(
            prompt=prompt,
            prompt_type=prompt_type,
            audience=payload.audience,
            output_style=payload.output_style,
            additional_context=payload.additional_context,
            file_context=payload.file_context,
        )

        improved_prompt = self.improver.build_improved_prompt(
            original_prompt=prompt,
            prompt_type=prompt_type,
            hidden_goal=hidden_goal,
            missing_pieces=missing_pieces,
            audience=payload.audience or "general",
            output_style=payload.output_style or "structured",
            additional_context=payload.additional_context,
            file_context=payload.file_context,
        )

        explanation = self.explainer.generate_explanation(
            prompt_type=prompt_type,
            missing_pieces=missing_pieces,
        )

        variants = self.variant_generator.generate(
            improved_prompt=improved_prompt,
            audience=payload.audience or "general",
        )

        score = 0.6

        if payload.additional_context:
            score += 0.1

        if payload.file_context:
            score += 0.1

        if len(prompt.split()) > 5:
            score += 0.1

        score = min(score, 0.95)

        expected_output_preview = self.preview_service.generate_preview(prompt_type)

        return PromptImproveResponse(
            original_prompt=prompt,
            prompt_type=prompt_type,
            hidden_goal=hidden_goal,
            missing_pieces=missing_pieces,
            improved_prompt=improved_prompt,
            explanation=explanation,
            confidence_score=min(score, 0.95),
            variants=[PromptVariant(**variant) for variant in variants],
            expected_output_preview=expected_output_preview,
        )