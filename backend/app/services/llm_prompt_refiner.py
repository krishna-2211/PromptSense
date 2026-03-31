from typing import Any, Optional

from app.services.llm_service import LLMService


class LLMPromptRefiner:
    def __init__(self) -> None:
        self.llm = LLMService()

    def is_available(self) -> bool:
        return self.llm.is_available()
    
    def _normalize_prompt_type(self, prompt_type: str, fallback: str) -> str:
        mapping = {
            "resume_bullet_point_generation": "resume_writing",
            "resume": "resume_writing",
            "email": "communication",
            "message": "communication",
            "study_plan": "planning",
            "study": "learning",
        }
        return mapping.get(prompt_type, prompt_type if prompt_type else fallback)

    def _looks_like_final_output(self, text: str) -> bool:
        if not text:
            return False

        lowered = text.lower().strip()

        bad_starts = [
            "as a ",
            "during my",
            "i successfully",
            "i analyzed",
            "i reduced",
            "dear ",
            "hi ",
            "hello ",
            "machine learning is",
            "week 1:",
            "•",
        ]

        good_starts = [
            "generate",
            "write",
            "summarize",
            "analyze",
            "explain",
            "create",
            "rewrite",
        ]

        if any(lowered.startswith(g) for g in good_starts):
            return False

        if any(lowered.startswith(b) for b in bad_starts):
            return True

        return False
    
    def refine(
        self,
        original_prompt: str,
        initial_prompt_type: str,
        missing_pieces: list[str],
        audience: str,
        output_style: str,
        additional_context: Optional[str] = None,
        file_context: Optional[str] = None,
    ) -> dict[str, Any]:
        if not self.llm.is_available():
            return {
                "prompt_type": initial_prompt_type,
                "hidden_goal": None,
                "improved_prompt": None,
                "variants": None,
                "expected_output_preview": None,
            }

        system_prompt = """
You are an expert prompt engineer and instruction optimizer.

Your task is NOT to answer the user's request.
Your task is NOT to generate the final content.
Your task is ONLY to generate the best possible PROMPT that the user can paste into an LLM like ChatGPT, Claude, or Gemini.

You will receive:
- the original user prompt
- an initial rule-based prompt type
- detected missing pieces
- audience
- output style
- optional additional context
- optional file context

Your job:
1. Refine the prompt type only if needed.
2. Infer the user's hidden goal.
3. Generate an optimized PROMPT for an LLM.
4. Generate 3 prompt variants:
   - Concise
   - Detailed
   - Professional
5. Generate a short expected output preview.

Critical rules:
- Do NOT perform the task.
- Do NOT write the final answer.
- Do NOT generate resume bullets, emails, summaries, or analysis results directly.
- Instead, write the instruction that would help another LLM generate the best answer.
- The improved_prompt must always sound like a user instruction to an LLM.
- Start the improved_prompt with action-oriented wording such as:
  "Generate...", "Write...", "Summarize...", "Analyze...", "Explain...", "Create..."
- expected_output_preview must be a short sample of what a good LLM answer might look like.
- expected_output_preview must be a single string, not an object.

Allowed prompt_type values:
- resume_writing
- communication
- summarization
- analysis
- planning
- learning
- writing
- general

Return ONLY valid JSON in this exact shape:
{
  "prompt_type": "string",
  "hidden_goal": "string",
  "improved_prompt": "string",
  "variants": [
    {"label": "Concise", "prompt": "string"},
    {"label": "Detailed", "prompt": "string"},
    {"label": "Professional", "prompt": "string"}
  ],
  "expected_output_preview": "string"
}
"""

        trimmed_file_context = file_context[:1200] if file_context else None

        user_prompt = f"""
Original user prompt:
{original_prompt}

Initial rule-based prompt type:
{initial_prompt_type}

Detected missing pieces:
{missing_pieces}

Audience:
{audience}

Output style:
{output_style}

Additional context:
{additional_context if additional_context else "None"}

File context:
{trimmed_file_context if trimmed_file_context else "None"}
"""

        try:
            result = self.llm.generate_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )

            prompt_type = self._normalize_prompt_type(
                result.get("prompt_type"),
                initial_prompt_type,
            )

            improved_prompt = result.get("improved_prompt")
            if self._looks_like_final_output(improved_prompt or ""):
                improved_prompt = None

            preview = result.get("expected_output_preview")
            if isinstance(preview, dict):
                preview = "\n".join(
                    [f"{label}: {text}" for label, text in preview.items()]
                )

            variants = result.get("variants")
            if isinstance(variants, list):
                cleaned_variants = []
                for variant in variants:
                    variant_prompt = variant.get("prompt", "")
                    if self._looks_like_final_output(variant_prompt):
                        continue
                    cleaned_variants.append(variant)
                variants = cleaned_variants if cleaned_variants else None

            return {
                "prompt_type": prompt_type,
                "hidden_goal": result.get("hidden_goal"),
                "improved_prompt": improved_prompt,
                "variants": variants,
                "expected_output_preview": preview,
            }
        except Exception:
            return {
                "prompt_type": initial_prompt_type,
                "hidden_goal": None,
                "improved_prompt": None,
                "variants": None,
                "expected_output_preview": None,
            }