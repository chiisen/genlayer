from fastapi import APIRouter

router = APIRouter()

from app.api.tasks import router as tasks_router  # noqa: E402
from app.api.video import router as video_router  # noqa: E402

router.include_router(video_router)
router.include_router(tasks_router)
