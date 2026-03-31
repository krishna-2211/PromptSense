from app.mcp.adapters.file_context_adapter import FileContextAdapter
from app.mcp.adapters.web_context_adapter import WebContextAdapter
from app.prompt_engine.classifier import classify_prompt_type
from app.prompt_engine.context_detector import detect_missing_pieces, extract_hidden_goal
from app.schemas.prompt_request import PromptImproveRequest
from app.schemas.prompt_response import PromptImproveResponse, PromptVariant
from app.services.explanation_service import ExplanationService
from app.services.llm_prompt_refiner import LLMPromptRefiner
from app.services.output_preview_service import OutputPreviewService
from app.services.prompt_improver import PromptImprover
from app.services.variant_generator import VariantGenerator


class PromptOrchestrator:
    def __init__(self) -> None:
        self.improver = PromptImprover()
        self.explainer = ExplanationService()
        self.variant_generator = VariantGenerator()
        self.preview_service = OutputPreviewService()
        self.llm_refiner = LLMPromptRefiner()

        self.file_context_adapter = FileContextAdapter()
        self.web_context_adapter = WebContextAdapter()

    def improve_prompt(self, payload: PromptImproveRequest) -> PromptImproveResponse:
        prompt = payload.original_prompt.strip()
        if not prompt:
            raise ValueError("Prompt cannot be empty.")

        used_context_sources: list[str] = []

        resolved_file_context = payload.file_context
        resolved_web_context = None

        if payload.file_id:
            try:
                resolved_file_context = self.file_context_adapter.get_context(payload.file_id)
                if resolved_file_context:
                    used_context_sources.append("file")
            except Exception as exc:
                print("File MCP failed:", str(exc))
                resolved_file_context = None

        if payload.web_url:
            try:
                resolved_web_context = self.web_context_adapter.get_context(payload.web_url)
                if resolved_web_context:
                    used_context_sources.append("web")
            except Exception as exc:
                print("Playwright MCP failed:", str(exc))
                resolved_web_context = None

        combined_context_parts: list[str] = []

        if payload.additional_context:
            combined_context_parts.append(payload.additional_context.strip())

        if resolved_web_context:
            combined_context_parts.append(resolved_web_context[:2500])

        combined_additional_context = (
            "\n\n".join(combined_context_parts) if combined_context_parts else None
        )

        initial_prompt_type = classify_prompt_type(prompt)
        initial_hidden_goal = extract_hidden_goal(prompt, initial_prompt_type)

        missing_pieces = detect_missing_pieces(
            prompt=prompt,
            prompt_type=initial_prompt_type,
            audience=payload.audience,
            output_style=payload.output_style,
            additional_context=combined_additional_context,
            file_context=resolved_file_context,
        )

        reasoning_mode = "rule-based"

        llm_result = self.llm_refiner.refine(
            original_prompt=prompt,
            initial_prompt_type=initial_prompt_type,
            missing_pieces=missing_pieces,
            audience=payload.audience or "general",
            output_style=payload.output_style or "structured",
            additional_context=combined_additional_context,
            file_context=resolved_file_context,
        )

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
            additional_context=combined_additional_context,
            file_context=resolved_file_context,
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
        if combined_additional_context:
            score += 0.1
        if resolved_file_context:
            score += 0.1
        if len(prompt.split()) > 5:
            score += 0.1
        if reasoning_mode == "hybrid":
            score += 0.05
        score = min(score, 0.95)

        expected_output_preview = llm_preview or self.preview_service.generate_preview(
            refined_prompt_type
        )

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
            used_context_sources=used_context_sources,
            variants=[PromptVariant(**variant) for variant in variants],
        )