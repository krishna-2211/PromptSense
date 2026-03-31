import json
import os

import ollama


class LLMService:
    def __init__(self) -> None:
        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

    def is_available(self) -> bool:
        try:
            ollama.list()
            return True
        except Exception:
            return False

    def generate_json(self, system_prompt: str, user_prompt: str) -> dict:
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            format="json",
            options={"temperature": 0.3},
        )

        content = response["message"]["content"]
        if not content:
            raise ValueError("Ollama returned empty content.")

        return json.loads(content)