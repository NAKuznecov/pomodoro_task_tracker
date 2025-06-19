from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db_session
from cache import get_redis_connection
from repository import TaskRep, CacheTask, UserRepository
from service import TaskService
from service.auth import AuthService
from service.user import UserService


def get_tasks_repository(db_session: Session = Depends(get_db_session)) -> TaskRep:
    return TaskRep(db_session=db_session)


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

def get_user_repository(db_session: Session = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db_session)


def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository=user_repository)


def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository=user_repository)
