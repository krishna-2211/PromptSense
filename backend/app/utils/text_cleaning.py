def extract_subject(prompt: str) -> str:
    prompt = prompt.lower().strip()

    triggers = [
        "teach me",
        "explain",
        "learn",
        "understand",
        "what is",
    ]

    for t in triggers:
        if prompt.startswith(t):
            return prompt.replace(t, "").strip()

    return prompt