from dataclasses import dataclass
import datetime as dt
from datetime import timedelta
from os import access

from jose import jwt, JWTError

from app.exception import UserNotFoundException, UserIncorrectPasswordException, TokenNotCorrectException, \
    TokenExpiredException
from app.settings import Settings
from app.users.auth.client.google_client import GoogleClient
from app.users.auth.client.yandex import YandexClient
from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.models import UserProfile
from app.users.user_profile.repository import UserRepository
from app.users.user_profile.schema import UserCreateSchema


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    yandex_client: YandexClient

    def google_auth(self, code: str):
        user_data = self.google_client.get_user_info(code)
        print(user_data)
        if user := self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
            google_access_token=user_data.access_token,
            email=user_data.email,
            name=user_data.name,
        )
        created_user = self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    def yandex_auth(self, code: str):
        user_data = self.yandex_client.get_user_info(code)
        print(user_data)
        if user := self.user_repository.get_user_by_email(email=user_data.default_email):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
            yandex_access_token=user_data.access_token,
            email=user_data.default_email,
            name=user_data.name,
        )
        created_user = self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    def get_google_redirect_url(self):
        return self.settings.google_redirect_url

    def get_yandex_redirect_url(self):
        return self.settings.yandex_redirect_url

    def get_yandex_auth(self, code: str):
        print(code)

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserIncorrectPasswordException

    def generate_access_token(self, user_id) -> str:
        expires_data_unix = (dt.datetime.utcnow() + timedelta(days=7)).timestamp()
        token = jwt.encode(
            claims={'user_id': user_id, 'expire': expires_data_unix},
            key=self.settings.JWT_SECRET,
            algorithm=self.settings.JWT_ENCODE_ALGORITHM,
        )
        return token

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(access_token, key=self.settings.JWT_SECRET,
                                 algorithms=self.settings.JWT_ENCODE_ALGORITHM)
        except JWTError:
            raise TokenNotCorrectException
        if payload['expire'] < dt.datetime.utcnow().timestamp():
            raise TokenExpiredException
        return payload['user_id']
