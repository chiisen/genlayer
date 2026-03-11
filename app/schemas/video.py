
from pydantic import BaseModel, Field


class VideoGenerateRequest(BaseModel):
    prompt: str = Field(..., description="User's video generation prompt")
    duration: int = Field(default=5, ge=1, le=30, description="Video duration in seconds")
    ratio: str = Field(default="16:9", description="Video aspect ratio")


class VideoGenerateResponse(BaseModel):
    task_id: str
    status: str
