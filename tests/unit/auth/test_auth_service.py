import pytest

from app.users.auth.service import AuthService

pytestmark = pytest.mark.asyncio

async def test_get_google_redirect_url__success(auth_service):
    assert isinstance(auth_service, AuthService)

