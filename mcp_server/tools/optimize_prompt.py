from schemas.tool_input import OptimizePromptInput
from schemas.tool_output import OptimizePromptOutput


def optimize_prompt(structured_prompt: str, prompt_type: str) -> str:
    optimization_suffix = {
        "analysis": "Prioritize clarity, business relevance, and actionable insight.",
        "writing": "Ensure the final response is polished, audience-aware, and easy to use directly.",
        "summarization": "Keep the summary accurate, compact, and aligned with the user's likely intent.",
        "planning": "Make the plan practical, sequenced, and easy to follow.",
        "coding": "Make the answer implementation-ready and explicit about assumptions.",
        "communication": "Keep the response clear, recipient-aware, and purposeful.",
        "general": "Maximize clarity, structure, and usefulness.",
    }.get(prompt_type, "Maximize clarity and usefulness.")

    return f"{structured_prompt}\n\nOptimization goal: {optimization_suffix}"


def run_tool(data: dict) -> dict:
    parsed = OptimizePromptInput(**data)

    improved_prompt = optimize_prompt(
        structured_prompt=parsed.structured_prompt,
        prompt_type=parsed.prompt_type,
    )

    return OptimizePromptOutput(
        improved_prompt=improved_prompt
    ).model_dump()