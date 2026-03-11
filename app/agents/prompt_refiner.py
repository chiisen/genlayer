from openai import OpenAI

from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()


class PromptRefiner:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

    def refine(self, prompt: str) -> str:
        if not settings.openai_api_key:
            return self._fallback_refine(prompt)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            refined = response.choices[0].message.content
            logger.info(f"Refined prompt: {refined[:100]}...")
            return refined
        except Exception as e:
            logger.warning(f"OpenAI API failed, using fallback: {e}")
            return self._fallback_refine(prompt)

    def _get_system_prompt(self) -> str:
        return """You are an expert video prompt engineer.
Transform the user's vague description into a detailed, high-quality prompt for AI video generation.
Include: subject details, scene description, camera movement, lighting, style, and mood.
Output ONLY the refined prompt, no explanations."""

    def _fallback_refine(self, prompt: str) -> str:
        return f"{prompt}, high quality, detailed, professional cinematography, cinematic lighting"
