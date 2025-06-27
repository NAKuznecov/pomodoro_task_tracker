import dataclasses
from asyncio import all_tasks

from app.exception import TaskNotFoundException
from app.tasks.repository.cache_task import CacheTask
from app.tasks.repository.task_rep import TaskRep
from app.tasks.schema import STask, TaskCreateSchema


@dataclasses.dataclass
class TaskService:
    def __init__(self, task_repository: TaskRep, task_cache: CacheTask):
        self.task_repository = task_repository
        self.task_cache = task_cache

    async def get_tasks(self) -> list[STask]:
        if cache_task := await self.task_cache.get_tasks():
            return cache_task
        else:
            tasks = await self.task_repository.get_tasks()
            tasks_schema = [STask.model_validate(task) for task in tasks]
            await self.task_cache.set_tasks(tasks_schema)
            return tasks_schema

    async def create_task(self, body: TaskCreateSchema, user_id: int) -> STask:
        task_id = await self.task_repository.create_task(body, user_id)
        task = await self.task_repository.get_task(task_id)
        return STask.model_validate(task)

    async def update_task_name(self, task_id: int, name: str, user_id: int) -> STask:
        task = await self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFoundException
        task = await self.task_repository.update_name(task_id=task_id, name=name)
        return STask.model_validate(task)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        task = await self.task_repository.get_user_task(task_id=task_id, user_id=user_id)
        if not task:
            raise TaskNotFoundException
        await self.task_repository.delete_task(task_id=task_id, user_id=user_id)
