class OutputPreviewService:
    def generate_preview(self, prompt_type: str) -> str:
        previews = {
            "resume_writing": (
                "• Increased reporting efficiency by 30% by automating dashboard workflows using Python, SQL, and Tableau.\n"
                "• Built data models that improved business visibility into customer trends and supported strategic decision-making."
            ),
            "communication": (
                "Hi [Name], I hope you're doing well. I wanted to reach out regarding..."
            ),
            "summarization": (
                "• Revenue increased by 12% quarter-over-quarter.\n"
                "• The main risk identified was declining retention in the mid-market segment.\n"
                "• Recommended next step: improve onboarding and retention campaigns."
            ),
            "analysis": (
                "• Sales dropped most sharply in the West region.\n"
                "• The main driver appears to be lower repeat purchases.\n"
                "• Recommended action: investigate retention and campaign performance."
            ),
            "planning": (
                "Week 1: Understand fundamentals and define goals.\n"
                "Week 2: Practice core concepts.\n"
                "Week 3: Apply learning through projects and review weak areas."
            ),
            "learning": (
                "Machine learning is a way of teaching computers to recognize patterns from data instead of explicitly programming every rule."
            ),
            "general": (
                "Here is a clearer, more structured response designed to better match your intended outcome."
            ),
        }

        return previews.get(prompt_type, previews["general"])