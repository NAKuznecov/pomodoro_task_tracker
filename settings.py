from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_DRIVER: str
    CACHE_HOST: str
    CACHE_PORT: int
    CACHE_DB: int
    JWT_SECRET: str
    JWT_ENCODE_ALGORITHM: str

    class Config:
        env_file = '.local.env'

    @property
    def db_url(self) -> str:
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
