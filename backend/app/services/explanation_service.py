from typing import List


class ExplanationService:
    def generate_explanation(self, prompt_type: str, missing_pieces: List[str]) -> str:
        labels = {
            "resume_writing": "resume writing",
            "communication": "professional communication",
            "summarization": "summarization",
            "analysis": "analysis",
            "planning": "planning",
            "learning": "learning",
            "writing": "writing",
            "general": "general assistance",
        }

        readable_type = labels.get(prompt_type, prompt_type.replace("_", " "))

        if missing_pieces:
            return (
                f"PromptSense identified this as a {readable_type} task and optimized it by adding the kind of details "
                f"LLMs need for better output, such as {', '.join(missing_pieces)}. "
                "Instead of only rephrasing your input, it rebuilt the instruction to be more specific, structured, and result-oriented."
            )

        return (
            f"PromptSense identified this as a {readable_type} task and improved it by making the instruction clearer, "
            "more structured, and better aligned with the output you are likely trying to get from the LLM."
        )