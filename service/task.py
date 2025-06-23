import dataclasses

from exception import TaskNotFoundException
from repository import TaskRep, CacheTask
from schema import TaskCreateSchema
from schema.s_task import STask


@dataclasses.dataclass
class TaskService:
    def __init__(self, task_repository: TaskRep, task_cache: CacheTask):
        self.task_repository = task_repository
        self.task_cache = task_cache

    def get_tasks(self) -> list[STask]:
        if cache_task := self.task_cache.get_tasks():
            return cache_task
        else:
            tasks = self.task_repository.get_tasks()
            tasks_schema = [STask.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(tasks_schema)
            return tasks_schema

    def create_task(self, body: TaskCreateSchema, user_id: int) -> STask:
        task_id = self.task_repository.create_task(body, user_id)
        task = self.task_repository.get_task(task_id)
        return STask.model_validate(task)

    def update_task_name(self, task_id: int, name: str, user_id: int) -> STask:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFoundException
        task = self.task_repository.update_name(task_id=task_id, name=name)
        return STask.model_validate(task)

    def delete_task(self, task_id: int, user_id: int) -> None:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise TaskNotFoundException
        self.task_repository.delete_task(task_id=task_id, user_id=user_id)
