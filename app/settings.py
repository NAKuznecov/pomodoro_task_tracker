from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = '0.0.0.0'
    DB_PORT: int = 5432
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'password'
    DB_NAME: str = 'pomodoro'
    DB_DRIVER: str = 'postgresql+asyncpg'
    CACHE_HOST: str = '0.0.0.0'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    JWT_SECRET: str = 'secret_key'
    JWT_ENCODE_ALGORITHM: str = 'HS256'
    GOOGLE_CLIENT_ID: str = '53131542715-eh880d8ul370ijuh0c2gvmlfganq11cb.apps.googleusercontent.com'
    GOOGLE_SECRET_KEY: str = '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'
    GOOGLE_REDIRECT_URI: str = 'http://localhost:8000/api/v1/oauth/google'
    GOOGLE_TOKEN_URL: str = "https://accounts.google.com/o/oauth2/token"
    YANDEX_CLIENT_ID: str = 'f9beceb4e6024f7d8b7b7c3d75779920'
    YANDEX_SECRET_KEY: str = '8da9c98ac3b5465284b5ddfd0253898d'
    YANDEX_REDIRECT_URI: str = 'http://localhost:8000/auth/yandex'
    YANDEX_TOKEN_URL: str = "https://oauth.yandex.ru/token"

    class Config:
        env_file = '../.local.env'

    @property
    def db_url(self) -> str:
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def google_redirect_url(self) -> str:
        return f'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline'

    @property
    def yandex_redirect_url(self) -> str:
        return f'https://oauth.yandex.ru/authorize?response_type=code&client_id={self.YANDEX_CLIENT_ID}&redirect_uri={self.YANDEX_REDIRECT_URI}&force_confirm=yes'