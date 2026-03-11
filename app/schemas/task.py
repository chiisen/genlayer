from enum import StrEnum

from pydantic import BaseModel


class TaskStatus(StrEnum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(BaseModel):
    task_id: str
    status: TaskStatus
    prompt: str
    refined_prompt: str | None = None
    video_url: str | None = None
    error: str | None = None
    created_at: float
    updated_at: float


class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    video_url: str | None = None
    error: str | None = None
