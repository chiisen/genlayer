from fastapi import APIRouter, HTTPException

from app.schemas.task import TaskResponse
from app.services.redis_task import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    task_service = TaskService()
    task = await task_service.get_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(
        task_id=task.task_id,
        status=task.status,
        video_url=task.video_url,
        error=task.error,
    )
