from typing import List, Optional
from app.utils.text_cleaning import extract_subject


class PromptImprover:
    def build_improved_prompt(
        self,
        original_prompt: str,
        prompt_type: str,
        hidden_goal: str,
        missing_pieces: List[str],
        audience: str,
        output_style: str,
        additional_context: Optional[str] = None,
        file_context: Optional[str] = None,
    ) -> str:
        if prompt_type == "resume_writing":
            return self._build_resume_prompt(additional_context, file_context)

        if prompt_type == "communication":
            return self._build_communication_prompt(original_prompt, audience, output_style, additional_context)

        if prompt_type == "summarization":
            return self._build_summarization_prompt(audience, output_style, additional_context, file_context)

        if prompt_type == "analysis":
            return self._build_analysis_prompt(audience, output_style, additional_context, file_context)

        if prompt_type == "planning":
            return self._build_planning_prompt(original_prompt, audience, output_style, additional_context)

        if prompt_type == "learning":
            return self._build_learning_prompt(original_prompt, audience, output_style, additional_context)

        return self._build_general_prompt(original_prompt, audience, output_style, additional_context, missing_pieces)

    def _build_resume_prompt(self, additional_context, file_context):
        prompt = (
            "Generate 3 ATS-optimized resume bullet points for a data analyst role.\n\n"
            "Each bullet should:\n"
            "- start with a strong action verb\n"
            "- include measurable impact (%, $, time saved)\n"
            "- mention relevant tools (SQL, Python, Tableau, Excel)\n"
            "- highlight business or analytical impact\n\n"
            "Keep bullets concise, professional, and achievement-oriented."
        )

        if additional_context:
            prompt += f"\n\nUse this context:\n{additional_context}"

        if file_context:
            prompt += f"\n\nUse relevant details from:\n{file_context[:500]}"

        return prompt

    def _build_communication_prompt(
        self,
        original_prompt: str,
        audience: str,
        output_style: str,
        additional_context: Optional[str],
    ) -> str:
        prompt = (
        "Write a clear, professional message.\n\n"
        f"Audience: {audience}\n"
        f"Tone: {output_style}\n\n"
        "Ensure the message is concise, well-structured, and purpose-driven."
    )

        if additional_context:
            prompt += f"\n\nContext:\n{additional_context}"

        return prompt

    def _build_summarization_prompt(
        self,
        audience: str,
        output_style: str,
        additional_context: Optional[str],
        file_context: Optional[str],
    ) -> str:
        prompt = (
            f"Summarize the provided material for a {audience} audience. "
            f"Use a {output_style} style and focus on key ideas, risks, and actionable takeaways."
        )

        if additional_context:
            prompt += f" Additional context: {additional_context.strip()}."

        if file_context:
            prompt += f" Base the summary on this source content: {file_context.strip()[:700]}..."

        prompt += " Present the summary in a clear, structured format."
        return prompt

    def _build_analysis_prompt(
        self,
        audience: str,
        output_style: str,
        additional_context: Optional[str],
        file_context: Optional[str],
    ) -> str:
        prompt = (
            "Analyze the provided data or subject and generate meaningful insights.\n\n"
            "Focus on:\n"
            "- key patterns and trends\n"
            "- anomalies or unusual behavior\n"
            "- possible causes\n"
            "- actionable recommendations\n\n"
            "Present findings in a structured format using bullet points or sections."
        )

        if additional_context:
            prompt += f"\n\nContext:\n{additional_context}"

        if file_context:
            prompt += f"\n\nData source:\n{file_context[:500]}"

        return prompt

    def _build_planning_prompt(
        self,
        original_prompt: str,
        audience: str,
        output_style: str,
        additional_context: Optional[str],
    ) -> str:
        prompt = (
            "Create a structured, step-by-step plan.\n\n"
            "Ensure the plan includes:\n"
            "- clear phases or steps\n"
            "- priorities\n"
            "- timeline or sequence\n"
            "- practical execution guidance\n"
        )

        if additional_context:
            prompt += f"\n\nContext:\n{additional_context}"

        return prompt

    def _build_learning_prompt(
        self,
        original_prompt: str,
        audience: str,
        output_style: str,
        additional_context: Optional[str],
    ) -> str:
        
        subject = extract_subject(original_prompt)

        prompt = (
            f"Explain {subject} in a structured, easy-to-understand way for a {audience} audience. "
            f"Use a {output_style} style. "
            "Start with intuition, then build concepts step by step, and include examples where helpful. "
            "Avoid unnecessary jargon and keep the explanation clear."
        )

        if additional_context:
            prompt += f" Additional context: {additional_context.strip()}."

        return prompt

    def _build_general_prompt(
        self,
        original_prompt: str,
        audience: str,
        output_style: str,
        additional_context: Optional[str],
        missing_pieces: List[str],
    ) -> str:
        prompt = (
            f"Help with this request: {original_prompt.strip()}. "
            f"Respond for a {audience} audience using a {output_style} format."
        )

        if additional_context:
            prompt += f" Additional context: {additional_context.strip()}."

        if missing_pieces:
            prompt += f" Fill in reasonable assumptions where needed, especially around: {', '.join(missing_pieces)}."

        prompt += " Make the response clear, specific, and directly useful."
        return prompt