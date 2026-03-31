from typing import Optional

def extract_hidden_goal(prompt: str, prompt_type: str) -> str:
    mapping = {
        "resume_writing": "Create strong, achievement-focused, ATS-friendly resume content tailored to a target role",
        "communication": "Create clear, effective, audience-appropriate communication",
        "summarization": "Condense source material into a useful summary for the intended audience",
        "analysis": "Generate structured insights, patterns, and actionable takeaways",
        "planning": "Create a practical, structured, executable plan",
        "learning": "Explain or teach a concept in a clear, structured, level-appropriate way",
        "writing": "Produce polished written content aligned with the user's purpose",
        "general": "Help the user express their intent clearly and effectively",
    }
    return mapping.get(prompt_type, mapping["general"])


def detect_missing_pieces(
    prompt: str,
    prompt_type: str,
    audience: Optional[str],
    output_style: Optional[str],
    additional_context: Optional[str],
    file_context: Optional[str],
) -> list[str]:
    missing: list[str] = []
    prompt_lower = prompt.lower().strip()

    if prompt_type == "resume_writing":
        if "data analyst" not in prompt_lower and "role" not in prompt_lower:
            missing.append("target role")
        if not additional_context and not file_context:
            missing.append("work experience details")
        missing.append("measurable impact")
        missing.append("key tools or skills")

    elif prompt_type == "communication":
        if not any(word in prompt_lower for word in ["recruiter", "manager", "team", "client", "professor"]):
            missing.append("recipient")
        if not additional_context:
            missing.append("purpose or context")
        missing.append("desired tone")

    elif prompt_type == "summarization":
        if not additional_context and not file_context:
            missing.append("source content")
        missing.append("summary focus")
        missing.append("summary format")

    elif prompt_type == "analysis":
        if not additional_context and not file_context:
            missing.append("dataset or business context")
        missing.append("analysis objective")
        missing.append("desired output format")

    elif prompt_type == "planning":
        missing.append("timeframe")
        missing.append("goal")
        missing.append("constraints or priorities")

    elif prompt_type == "learning":
        missing.append("knowledge level")
        missing.append("learning goal")
        missing.append("preferred explanation style")

    else:
        if len(prompt.split()) < 4:
            missing.append("clear objective")
        if not additional_context and not file_context:
            missing.append("supporting context")

    # dedupe
    final = []
    seen = set()
    for item in missing:
        if item not in seen:
            final.append(item)
            seen.add(item)

    return final