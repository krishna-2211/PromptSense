class VariantGenerator:
    def generate(self, improved_prompt: str, audience: str) -> list[dict[str, str]]:
        concise = f"{improved_prompt}\n\nKeep the response concise and to the point."
        detailed = f"{improved_prompt}\n\nProvide a detailed response with deeper explanation where relevant."
        professional = (
            f"{improved_prompt}\n\nUse a polished, professional tone appropriate for {audience}."
        )

        return [
            {"label": "Concise", "prompt": concise},
            {"label": "Detailed", "prompt": detailed},
            {"label": "Professional", "prompt": professional},
        ]