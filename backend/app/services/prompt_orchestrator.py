from app.schemas.prompt_request import PromptImproveRequest
from app.schemas.prompt_response import PromptImproveResponse, PromptVariant
from app.services.prompt_improver import PromptImprover
from app.services.explanation_service import ExplanationService
from app.services.variant_generator import VariantGenerator
from app.services.output_preview_service import OutputPreviewService
from app.services.llm_prompt_refiner import LLMPromptRefiner
from app.prompt_engine.classifier import classify_prompt_type
from app.prompt_engine.context_detector import detect_missing_pieces, extract_hidden_goal


class PromptOrchestrator:
    def __init__(self) -> None:
        self.improver = PromptImprover()
        self.explainer = ExplanationService()
        self.variant_generator = VariantGenerator()
        self.preview_service = OutputPreviewService()
        self.llm_refiner = LLMPromptRefiner()

    def improve_prompt(self, payload: PromptImproveRequest) -> PromptImproveResponse:
        prompt = payload.original_prompt.strip()
        if not prompt:
            raise ValueError("Prompt cannot be empty.")

        initial_prompt_type = classify_prompt_type(prompt)
        initial_hidden_goal = extract_hidden_goal(prompt, initial_prompt_type)

        missing_pieces = detect_missing_pieces(
            prompt=prompt,
            prompt_type=initial_prompt_type,
            audience=payload.audience,
            output_style=payload.output_style,
            additional_context=payload.additional_context,
            file_context=payload.file_context,
        )

        reasoning_mode = "rule-based"

        llm_result = self.llm_refiner.refine(
            original_prompt=prompt,
            initial_prompt_type=initial_prompt_type,
            missing_pieces=missing_pieces,
            audience=payload.audience or "general",
            output_style=payload.output_style or "structured",
            additional_context=payload.additional_context,
            file_context=payload.file_context,
        )

        print("LLM RESULT:", llm_result)

        refined_prompt_type = llm_result.get("prompt_type") or initial_prompt_type
        refined_hidden_goal = llm_result.get("hidden_goal") or initial_hidden_goal

        llm_improved_prompt = llm_result.get("improved_prompt")
        llm_variants = llm_result.get("variants")
        llm_preview = llm_result.get("expected_output_preview")

        if llm_improved_prompt:
            reasoning_mode = "hybrid"

        improved_prompt = llm_improved_prompt or self.improver.build_improved_prompt(
            original_prompt=prompt,
            prompt_type=refined_prompt_type,
            hidden_goal=refined_hidden_goal,
            missing_pieces=missing_pieces,
            audience=payload.audience or "general",
            output_style=payload.output_style or "structured",
            additional_context=payload.additional_context,
            file_context=payload.file_context,
        )

        explanation = self.explainer.generate_explanation(
            prompt_type=refined_prompt_type,
            missing_pieces=missing_pieces,
        )

        variants = llm_variants or self.variant_generator.generate(
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
        if reasoning_mode == "hybrid":
            score += 0.05
        score = min(score, 0.95)

        expected_output_preview = llm_preview or self.preview_service.generate_preview(
            refined_prompt_type
        )

        print("REASONING MODE:", reasoning_mode)

        return PromptImproveResponse(
            original_prompt=prompt,
            prompt_type=refined_prompt_type,
            hidden_goal=refined_hidden_goal,
            missing_pieces=missing_pieces,
            improved_prompt=improved_prompt,
            explanation=explanation,
            confidence_score=round(score, 2),
            expected_output_preview=expected_output_preview,
            reasoning_mode=reasoning_mode,
            variants=[PromptVariant(**variant) for variant in variants],
        )