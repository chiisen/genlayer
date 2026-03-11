from fastapi import APIRouter

from app.schemas.video import VideoGenerateRequest, VideoGenerateResponse
from app.services.redis_task import TaskService

router = APIRouter(prefix="/video", tags=["video"])


@router.post("/generate", response_model=VideoGenerateResponse)
async def generate_video(request: VideoGenerateRequest):
    task_service = TaskService()

    task = await task_service.create_task(request.prompt)

    return VideoGenerateResponse(
        task_id=task.task_id,
        status=task.status.value,
    )
