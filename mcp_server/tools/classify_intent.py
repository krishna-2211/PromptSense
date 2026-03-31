from schemas.tool_input import ClassifyIntentInput
from schemas.tool_output import ClassifyIntentOutput


def classify_prompt_type(prompt: str) -> str:
    prompt_lower = prompt.lower()

    analysis_keywords = ["analyze", "insight", "trend", "data", "dataset", "findings"]
    writing_keywords = ["write", "draft", "rewrite", "improve", "edit", "bullet"]
    summary_keywords = ["summarize", "summary", "condense", "tl;dr"]
    planning_keywords = ["plan", "roadmap", "steps", "strategy", "schedule"]
    coding_keywords = ["code", "python", "sql", "bug", "debug", "function", "script"]
    communication_keywords = ["email", "message", "reply", "follow up", "outreach"]

    if any(word in prompt_lower for word in analysis_keywords):
        return "analysis"
    if any(word in prompt_lower for word in writing_keywords):
        return "writing"
    if any(word in prompt_lower for word in summary_keywords):
        return "summarization"
    if any(word in prompt_lower for word in planning_keywords):
        return "planning"
    if any(word in prompt_lower for word in coding_keywords):
        return "coding"
    if any(word in prompt_lower for word in communication_keywords):
        return "communication"

    return "general"


def extract_hidden_goal(prompt_type: str) -> str:
    mapping = {
        "analysis": "Analyze the subject thoroughly and surface meaningful insights",
        "writing": "Produce polished written content aligned with the user's purpose",
        "summarization": "Summarize the source material clearly and accurately",
        "planning": "Create a practical step-by-step plan",
        "coding": "Provide implementation-oriented technical help",
        "communication": "Craft a clear and effective communication message",
        "general": "Help the user accomplish their intended task more clearly",
    }
    return mapping.get(prompt_type, mapping["general"])


def run_tool(data: dict) -> dict:
    parsed = ClassifyIntentInput(**data)
    prompt_type = classify_prompt_type(parsed.prompt)
    hidden_goal = extract_hidden_goal(prompt_type)

    return ClassifyIntentOutput(
        prompt_type=prompt_type,
        hidden_goal=hidden_goal,
    ).model_dump()