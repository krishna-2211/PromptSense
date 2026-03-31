from schemas.tool_input import StructureInstructionInput
from schemas.tool_output import StructureInstructionOutput


def build_structured_prompt(
    original_prompt: str,
    prompt_type: str,
    hidden_goal: str,
    missing_pieces: list[str],
    audience: str,
    output_style: str,
    additional_context: str | None = None,
    file_context: str | None = None,
) -> str:
    sections: list[str] = []

    sections.append(f"Task: {hidden_goal}.")
    sections.append(f"Original request: {original_prompt.strip()}.")
    sections.append(f"Target audience: {audience}.")
    sections.append(f"Response style: {output_style}.")

    if additional_context:
        sections.append(f"Additional context: {additional_context.strip()}.")

    if file_context:
        trimmed = file_context.strip()
        shortened = trimmed[:800] + ("..." if len(trimmed) > 800 else "")
        sections.append(f"Use this source context when relevant: {shortened}")

    if missing_pieces:
        missing_text = ", ".join(missing_pieces)
        sections.append(
            "While answering, make reasonable assumptions only where needed and "
            f"be explicit about these missing elements: {missing_text}."
        )

    type_instructions = get_type_specific_instructions(prompt_type)
    if type_instructions:
        sections.append(type_instructions)

    sections.append(
        "Provide a clear, useful, well-structured response that directly helps the user accomplish the task."
    )

    return "\n\n".join(sections)


def get_type_specific_instructions(prompt_type: str) -> str:
    mapping = {
        "analysis": (
            "Focus on identifying patterns, key findings, and actionable insights. "
            "Use structured bullets or sections."
        ),
        "writing": (
            "Use strong clarity, tone, and structure. Ensure the output is polished and audience-appropriate."
        ),
        "summarization": (
            "Capture the main ideas accurately, avoid unnecessary detail, and preserve important context."
        ),
        "planning": (
            "Break the response into clear steps, sequence them logically, and make the plan practical."
        ),
        "coding": (
            "Provide implementation-ready guidance, explain assumptions, and include structured code when useful."
        ),
        "communication": (
            "Keep the tone appropriate, the message concise, and the intent easy for the recipient to understand."
        ),
        "general": (
            "Clarify the request, add structure, and make the expected response more specific and useful."
        ),
    }
    return mapping.get(prompt_type, mapping["general"])


def run_tool(data: dict) -> dict:
    parsed = StructureInstructionInput(**data)

    structured_prompt = build_structured_prompt(
        original_prompt=parsed.original_prompt,
        prompt_type=parsed.prompt_type,
        hidden_goal=parsed.hidden_goal,
        missing_pieces=parsed.missing_pieces,
        audience=parsed.audience or "general",
        output_style=parsed.output_style or "structured",
        additional_context=parsed.additional_context,
        file_context=parsed.file_context,
    )

    return StructureInstructionOutput(
        structured_prompt=structured_prompt
    ).model_dump()