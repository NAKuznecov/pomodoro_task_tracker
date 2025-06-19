import dataclasses

from repository import TaskRep, CacheTask
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