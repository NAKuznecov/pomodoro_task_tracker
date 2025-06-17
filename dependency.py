from fastapi import Depends
from database import get_db_session
from cache import get_redis_connection
from repository import TaskRep, CacheTask
from service import TaskService


def get_tasks_repository() -> TaskRep:
    db_session = get_db_session()
    return TaskRep(db_session)


def get_cache_repository() -> CacheTask:
    redis_connection = get_redis_connection()
    return CacheTask(redis_connection)


def get_task_service(
        task_repository: TaskRep = Depends(get_tasks_repository),
        task_cache: CacheTask = Depends(get_cache_repository)
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache
    )
