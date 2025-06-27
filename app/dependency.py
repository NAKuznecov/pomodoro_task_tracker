import httpx
from fastapi import Depends, security, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from app.exception import TokenExpiredException, TokenNotCorrectException
from app.infrastructure.cache.accessor import get_redis_connection
from app.infrastructure.database.accessor import get_db_session
from app.settings import Settings
from app.tasks.repository.cache_task import CacheTask
from app.tasks.repository.task_rep import TaskRep
from app.tasks.service import TaskService
from app.users.auth.client.google_client import GoogleClient
from app.users.auth.client.yandex import YandexClient
from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserRepository
from app.users.user_profile.service import UserService


async def get_tasks_repository(db_session: AsyncSession = Depends(get_db_session)) -> TaskRep:
    return TaskRep(db_session=db_session)


async def get_cache_repository() -> CacheTask:
    redis_connection = get_redis_connection()
    return CacheTask(redis_connection)


async def get_task_service(
        task_repository: TaskRep = Depends(get_tasks_repository),
        task_cache: CacheTask = Depends(get_cache_repository)
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache
    )


async def get_user_repository(db_session: Session = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db_session)


async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()


async def get_google_client(async_client: httpx.AsyncClient = Depends(get_async_client)) -> GoogleClient:
    return GoogleClient(settings=Settings(), async_client=async_client)


async def get_yandex_client(async_client: httpx.AsyncClient = Depends(get_async_client)) -> YandexClient:
    return YandexClient(settings=Settings(), async_client=async_client)


async def get_auth_service(
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


async def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
        auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_oauth2 = security.HTTPBearer()


async def get_request_user_id(
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
