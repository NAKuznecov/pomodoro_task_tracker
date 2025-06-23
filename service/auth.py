from dataclasses import dataclass
import datetime as dt
from datetime import timedelta

from jose import jwt, JWTError

from cache.accessor import settings
from exception import UserNotFoundException, UserIncorrectPasswordException, TokenExpiredException, \
    TokenNotCorrectException
from models import UserProfile
from repository import UserRepository
from schema import UserLoginSchema
from settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings

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
