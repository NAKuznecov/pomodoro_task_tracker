from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependency import get_auth_service
from app.users.auth.service import AuthService

router = APIRouter(
    prefix="/api/v1",
    tags=["google_auth"],
)


@router.get(
    "/oauth/google",
)
async def google_auth(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        code: str
):
    return auth_service.google_auth(code=code)