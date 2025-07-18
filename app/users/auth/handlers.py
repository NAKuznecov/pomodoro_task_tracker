from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from starlette import status

from app.dependency import get_auth_service
from app.exception import UserNotFoundException, UserIncorrectPasswordException
from app.users.auth.schema import UserLoginSchema
from app.users.auth.service import AuthService
from app.users.user_profile.schema import UserCreateSchema

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/login",
    response_model=UserLoginSchema,
)
async def login(
        body: UserCreateSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        return await auth_service.login(body.username, body.password)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail,
        )
    except UserIncorrectPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail,
        )


# Гугл авторизация через OAuth2
@router.get(
    "/api/v1/login/google",
)
async def google_login(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    redirect_url = auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


# @router.get(
#     "/api/v1/oauth/google",
# )
# async def google_auth(
#         auth_service: Annotated[AuthService, Depends(get_auth_service)],
#         code: str
# ):
#     return auth_service.google_auth(code=code)


@router.get(
    "/login/yandex",
    response_class=RedirectResponse,
)
async def yandex_login(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    redirect_url = auth_service.get_yandex_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get(
    "/yandex"
)
async def yandex_auth(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        code: str
):
    return await auth_service.yandex_auth(code=code)
