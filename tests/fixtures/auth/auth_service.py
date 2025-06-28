
import pytest
import pytest_asyncio

from app.infrastructure.database import get_db_session
from app.settings import Settings
from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserRepository

db = get_db_session()
@pytest_asyncio.fixture
async def mock_auth_service(yandex_client, google_client, fake_user_repository):
    return AuthService(
        user_repository=fake_user_repository,
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
    )


@pytest_asyncio.fixture
async def auth_service(yandex_client, google_client, mock_auth_service):
    return AuthService(
        user_repository=UserRepository(db_session=db),
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
    )
