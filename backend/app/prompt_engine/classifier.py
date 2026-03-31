def classify_prompt_type(prompt: str) -> str:
    prompt_lower = prompt.lower().strip()

    if any(phrase in prompt_lower for phrase in [
        "resume bullet", "resume bullets", "rewrite my resume", "improve my resume", "resume"
    ]):
        return "resume_writing"

    if any(phrase in prompt_lower for phrase in [
        "write an email", "draft an email", "email to", "follow up", "linkedin message", "outreach"
    ]):
        return "communication"

    if any(phrase in prompt_lower for phrase in [
        "summarize", "summary", "condense", "tl;dr"
    ]):
        return "summarization"

    if any(phrase in prompt_lower for phrase in [
        "plan", "roadmap", "schedule", "steps", "strategy"
    ]):
        return "planning"

    if any(phrase in prompt_lower for phrase in [
        "learn", "teach me", "understand", "explain"
    ]):
        return "learning"

    if any(phrase in prompt_lower for phrase in [
        "analyze", "insight", "trend", "dataset", "findings", "why did", "what caused"
    ]):
        return "analysis"

    if any(phrase in prompt_lower for phrase in [
        "write", "draft", "rewrite", "edit"
    ]):
        return "writing"

    return "general"