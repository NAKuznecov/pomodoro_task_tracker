from fastapi import Depends, Request, security, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from client import GoogleClient, YandexClient
from database import get_db_session
from cache import get_redis_connection
from exception import TokenExpiredException, TokenNotCorrectException
from repository import TaskRep, CacheTask, UserRepository
from service import TaskService
from service.auth import AuthService
from service.user import UserService
from settings import Settings


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


def get_google_client() -> GoogleClient:
    return GoogleClient(settings=Settings())

def get_yandex_client() -> YandexClient:
    return YandexClient(settings=Settings())


def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
        google_client: GoogleClient = Depends(get_google_client),
        yandex_client: YandexClient = Depends(get_yandex_client),
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client
    )


def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_oauth2 = security.HTTPBearer()


def get_request_user_id(
        auth_service: AuthService = Depends(get_auth_service),
        token: security.http.HTTPAuthorizationCredentials = Depends(reusable_oauth2)
) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpiredException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )
    except TokenNotCorrectException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail,
        )
    return user_id
