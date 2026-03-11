import time
import uuid

import redis.asyncio as redis

from app.core.config import get_settings
from app.core.logging import logger
from app.core.redis import get_redis
from app.schemas.task import Task, TaskStatus

settings = get_settings()


class TaskService:
    def __init__(self, redis_client: redis.Redis | None = None):
        self.redis = redis_client
        self.ttl = settings.redis_task_ttl

    async def get_client(self) -> redis.Redis:
        if self.redis is None:
            self.redis = await get_redis()
        return self.redis

    async def create_task(self, prompt: str) -> Task:
        client = await self.get_client()
        task_id = str(uuid.uuid4())
        now = time.time()

        task = Task(
            task_id=task_id,
            status=TaskStatus.QUEUED,
            prompt=prompt,
            created_at=now,
            updated_at=now,
        )

        await client.set(
            f"task:{task_id}",
            task.model_dump_json(),
            ex=self.ttl,
        )
        logger.info(f"Created task: {task_id}")
        return task

    async def get_task(self, task_id: str) -> Task | None:
        client = await self.get_client()
        data = await client.get(f"task:{task_id}")

        if not data:
            return None

        return Task.model_validate_json(data)

    async def update_task(self, task_id: str, **kwargs) -> Task | None:
        client = await self.get_client()
        task = await self.get_task(task_id)

        if not task:
            return None

        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)

        task.updated_at = time.time()

        await client.set(
            f"task:{task_id}",
            task.model_dump_json(),
            ex=self.ttl,
        )
        logger.info(f"Updated task: {task_id}")
        return task
