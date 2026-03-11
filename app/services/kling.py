import httpx

from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()


class KlingClient:
    def __init__(self):
        self.base_url = settings.kling_base_url
        self.api_key = settings.kling_api_key

    async def generate_video(self, prompt: str, duration: int = 5, ratio: str = "16:9") -> dict:
        if not self.api_key:
            return self._mock_response(prompt, duration, ratio)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "prompt": prompt,
            "duration": duration,
            "ratio": ratio,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v1/generation/text2video",
                    headers=headers,
                    json=payload,
                    timeout=30.0,
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Kling API response: {result}")
                return result
        except Exception as e:
            logger.warning(f"Kling API failed, using mock: {e}")
            return self._mock_response(prompt, duration, ratio)

    def _mock_response(self, prompt: str, duration: int, ratio: str) -> dict:
        import uuid
        return {
            "task_id": str(uuid.uuid4()),
            "status": "processing",
            "message": "Video generation started",
        }
